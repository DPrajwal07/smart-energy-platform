# Smart Energy Platform - FastAPI Backend
# A simple and clean API for managing energy data

# Import FastAPI components
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime
import pandas as pd

# Import database components
from database import engine, Base, get_db
from models import EnergyReading
from schemas import EnergyReadingCreate, EnergyReadingResponse, ErrorResponse
from sqlalchemy.orm import Session

# Import analysis functions
from analysis import calculate_daily_consumption

# Import carbon footprint calculation
from carbon_footprint import calculate_co2_with_breakdown

# Import energy prediction model
from energy_prediction_model import EnergyConsumptionPredictor
from datetime import timedelta

# Note: Database tables will be created on first API call to database endpoints
# This prevents startup errors if PostgreSQL is not running yet
# To manually create tables, uncomment the line below:
# Base.metadata.create_all(bind=engine)

# ============================================================================
# Initialize FastAPI Application
# ============================================================================
# Create an instance of FastAPI with a title and description
app = FastAPI(
    title="Smart Energy Platform API",
    description="A simple API for managing smart energy data",
    version="1.0.0"
)

# ============================================================================
# Root Endpoint
# ============================================================================
# This is the main endpoint that greets users when they visit the API
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A JSON object with a greeting and current timestamp
    """
    return {
        "message": "Welcome to Smart Energy Platform API",
        "description": "Monitor and optimize your energy usage",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ============================================================================
# Health Check Endpoint
# ============================================================================
# This endpoint is used to check if the API is running and responsive
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring API status.
    
    This endpoint is typically called by:
    - Load balancers to verify the server is healthy
    - Monitoring systems to track uptime
    - Clients to confirm connectivity
    
    Returns:
        dict: A JSON object indicating the API is healthy
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# Database Energy Data Endpoint
# ============================================================================
# This endpoint retrieves energy readings from the PostgreSQL database
@app.get("/energy/readings")
def get_energy_readings(db: Session = Depends(get_db)):
    """
    Get all energy readings from the database.
    
    This endpoint demonstrates how to:
    1. Use dependency injection with Depends(get_db)
    2. Query the database using SQLAlchemy
    3. Return database results as JSON
    
    Parameters:
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        list: All energy readings from the database, or empty list if none exist
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Query all energy readings from the database
    readings = db.query(EnergyReading).all()
    
    # Convert SQLAlchemy objects to dictionaries for JSON response
    return [
        {
            "id": reading.id,
            "machine_id": reading.machine_id,
            "power_kw": reading.power_kw,
            "energy_consumed_kwh": reading.energy_consumed_kwh,
            "timestamp": reading.timestamp.isoformat() if reading.timestamp else None
        }
        for reading in readings
    ]

# ============================================================================
# Add Energy Reading Endpoint
# ============================================================================
# This endpoint demonstrates how to insert new data into the database
@app.post("/energy/readings")
def add_energy_reading(
    machine_id: str,
    power_kw: float,
    energy_consumed_kwh: float,
    db: Session = Depends(get_db)
):
    """
    Add a new energy reading to the database.
    
    This endpoint demonstrates how to:
    1. Accept query parameters from the API request
    2. Create a new database record
    3. Commit changes to the database
    
    Parameters:
        machine_id: Unique identifier for the machine
        power_kw: Current power consumption in kilowatts
        energy_consumed_kwh: Total energy consumed in kilowatt-hours
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        dict: The newly created reading with ID and timestamp
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a new EnergyReading object
    new_reading = EnergyReading(
        machine_id=machine_id,
        power_kw=power_kw,
        energy_consumed_kwh=energy_consumed_kwh
    )
    
    # Add the new reading to the session
    db.add(new_reading)
    
    # Commit changes to the database
    db.commit()
    
    # Refresh to get the auto-generated ID and timestamp
    db.refresh(new_reading)
    
    # Return the created reading
    return {
        "id": new_reading.id,
        "machine_id": new_reading.machine_id,
        "power_kw": new_reading.power_kw,
        "energy_consumed_kwh": new_reading.energy_consumed_kwh,
        "timestamp": new_reading.timestamp.isoformat() if new_reading.timestamp else None
    }

# ============================================================================
# Add Energy Reading via JSON (POST Endpoint)
# ============================================================================
# This endpoint accepts JSON input and stores data in PostgreSQL
@app.post(
    "/energy/add",
    response_model=EnergyReadingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add New Energy Reading",
    description="Create a new energy reading by sending JSON data"
)
def add_energy_reading_json(
    reading_data: EnergyReadingCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new energy reading via JSON POST request.
    
    This endpoint demonstrates:
    1. Accepting JSON input with Pydantic validation
    2. Error handling with HTTPException
    3. Storing data in PostgreSQL using SQLAlchemy
    4. Returning validated response data
    
    Request Body (JSON):
        {
            "machine_id": "MACHINE-001",
            "power_kw": 45.5,
            "energy_consumed_kwh": 1250.75
        }
    
    Response (201 Created):
        {
            "id": 1,
            "machine_id": "MACHINE-001",
            "power_kw": 45.5,
            "energy_consumed_kwh": 1250.75,
            "timestamp": "2026-01-26T10:30:00"
        }
    
    Raises:
        HTTPException: If database operation fails
    """
    try:
        # ====================================================================
        # Step 1: Create database tables if they don't exist
        # ====================================================================
        # This is a safety measure - in production, tables are pre-created
        Base.metadata.create_all(bind=engine)
        
        # ====================================================================
        # Step 2: Validate the input data
        # ====================================================================
        # Pydantic has already validated the JSON input before this function
        # Access the validated data from the reading_data object
        # Example: reading_data.machine_id, reading_data.power_kw
        
        # ====================================================================
        # Step 3: Create a new EnergyReading database record
        # ====================================================================
        # Convert the Pydantic model to a SQLAlchemy model
        new_reading = EnergyReading(
            machine_id=reading_data.machine_id,
            power_kw=reading_data.power_kw,
            energy_consumed_kwh=reading_data.energy_consumed_kwh
        )
        
        # ====================================================================
        # Step 4: Add the new record to the database session
        # ====================================================================
        # The session is a container that tracks changes to objects
        db.add(new_reading)
        
        # ====================================================================
        # Step 5: Commit the transaction to the database
        # ====================================================================
        # This saves the new record to PostgreSQL permanently
        db.commit()
        
        # ====================================================================
        # Step 6: Refresh the object with database-generated values
        # ====================================================================
        # This gets the auto-generated id and timestamp from the database
        db.refresh(new_reading)
        
        # ====================================================================
        # Step 7: Return the created reading
        # ====================================================================
        # Pydantic will automatically convert the SQLAlchemy object
        # to the EnergyReadingResponse format
        return new_reading
    
    # ========================================================================
    # ERROR HANDLING
    # ========================================================================
    except ValueError as e:
        # Handle validation errors (shouldn't happen with Pydantic, but just in case)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input data: {str(e)}"
        )
    
    except Exception as e:
        # Handle unexpected database or other errors
        # In production, log these errors for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save energy reading to database"
        )

# ============================================================================
# Energy Data Endpoint
# ============================================================================
# This endpoint returns sample industrial energy data for demonstration
@app.get("/energy/sample")
def get_energy_sample():
    """
    Get sample industrial energy data.
    
    This endpoint returns sample energy consumption data that demonstrates
    the structure of energy data in the Smart Energy Platform.
    
    Returns:
        dict: A JSON object containing:
            - machine_id: Unique identifier for the industrial machine
            - power_kw: Current power consumption in kilowatts
            - energy_consumed_kwh: Total energy consumed in kilowatt-hours
            - timestamp: ISO format timestamp of the data collection
    """
    return {
        "machine_id": "MACHINE-001",
        "power_kw": 45.5,
        "energy_consumed_kwh": 1250.75,
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# Analytics Endpoint - Daily Energy Consumption
# ============================================================================
# This endpoint analyzes energy data and returns daily consumption statistics
@app.get(
    "/analytics/daily",
    summary="Daily Energy Analysis",
    description="Analyze energy consumption data by day"
)
def get_daily_analytics(
    machine_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Get daily energy consumption analysis from PostgreSQL.
    
    This endpoint demonstrates:
    1. Querying data from PostgreSQL database
    2. Converting database results to Pandas DataFrame
    3. Using analysis functions to process data
    4. Returning results as JSON
    
    Parameters:
        machine_id: Optional filter for specific machine (e.g., "MACHINE-001")
                   If not provided, analyzes all machines
        db: Database session (automatically provided by FastAPI)
    
    Returns:
        dict: Analysis results with:
            - analysis_date: When the analysis was performed
            - machine_id: Which machine(s) were analyzed
            - data_points: Number of readings analyzed
            - daily_data: List of daily totals
            - summary: Statistics about the data
    
    Example response:
        {
            "analysis_date": "2026-01-26T10:30:00",
            "machine_id": "MACHINE-001",
            "data_points": 48,
            "daily_data": [
                {
                    "date": "2026-01-01",
                    "total_energy_kwh": 1250.75
                }
            ],
            "summary": {
                "average_daily_kwh": 1250.75,
                "min_daily_kwh": 1250.75,
                "max_daily_kwh": 1250.75,
                "total_days": 1
            }
        }
    """
    try:
        # ====================================================================
        # Step 1: Query energy readings from PostgreSQL
        # ====================================================================
        # Build the query - optionally filter by machine_id
        query = db.query(EnergyReading)
        
        if machine_id:
            # Filter by specific machine
            query = query.filter(EnergyReading.machine_id == machine_id)
        
        # Execute the query and get all results
        energy_readings = query.all()
        
        # ====================================================================
        # Step 2: Handle case when no data is found
        # ====================================================================
        if not energy_readings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No energy data found{f' for machine {machine_id}' if machine_id else ''}"
            )
        
        # ====================================================================
        # Step 3: Convert database results to Pandas DataFrame
        # ====================================================================
        # Transform SQLAlchemy objects into a dictionary for Pandas
        # Pandas needs standard Python types, not SQLAlchemy objects
        data_for_dataframe = [
            {
                'timestamp': reading.timestamp,
                'power_kw': reading.power_kw,
                'energy_consumed_kwh': reading.energy_consumed_kwh,
                'machine_id': reading.machine_id
            }
            for reading in energy_readings
        ]
        
        # Create the DataFrame from the list of dictionaries
        df = pd.DataFrame(data_for_dataframe)
        
        # ====================================================================
        # Step 4: Process data using analysis functions
        # ====================================================================
        # Use the calculate_daily_consumption function to aggregate by day
        daily_consumption = calculate_daily_consumption(
            df,
            date_column='timestamp',
            energy_column='energy_consumed_kwh'
        )
        
        # ====================================================================
        # Step 5: Calculate summary statistics
        # ====================================================================
        # These statistics describe the overall data
        summary_stats = {
            'average_daily_kwh': float(daily_consumption['total_energy_kwh'].mean()),
            'min_daily_kwh': float(daily_consumption['total_energy_kwh'].min()),
            'max_daily_kwh': float(daily_consumption['total_energy_kwh'].max()),
            'total_days': len(daily_consumption)
        }
        
        # ====================================================================
        # Step 6: Format the response
        # ====================================================================
        # Convert the daily consumption DataFrame to a list of dictionaries
        # This makes it JSON-serializable
        daily_data = [
            {
                'date': str(row['date']),
                'total_energy_kwh': float(row['total_energy_kwh'])
            }
            for _, row in daily_consumption.iterrows()
        ]
        
        # Build the response object
        response = {
            'analysis_date': datetime.now().isoformat(),
            'machine_id': machine_id or 'All Machines',
            'data_points': len(energy_readings),
            'daily_data': daily_data,
            'summary': summary_stats
        }
        
        return response
    
    # ========================================================================
    # ERROR HANDLING
    # ========================================================================
    except HTTPException:
        # Re-raise HTTP exceptions (like 404 Not Found)
        raise
    
    except Exception as e:
        # Handle unexpected errors (database issues, Pandas errors, etc.)
        # In production, log these errors for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing energy data: {str(e)}"
        )

# ============================================================================
# Carbon Footprint Endpoint
# ============================================================================
# Calculate CO2 emissions from energy consumption
# Shows environmental impact of energy usage

@app.get("/analytics/carbon", summary="Carbon Footprint Analysis", description="Calculate CO2 emissions from energy consumption data. Returns daily and monthly carbon footprint with regional variations.")
def get_carbon_footprint(
    machine_id: str = None,
    region: str = "US_Average",
    db: Session = Depends(get_db)
):
    """
    Calculate carbon footprint (CO2 emissions) from energy consumption.
    
    Parameters:
    -----------
    machine_id (optional):
        Filter results to specific machine. If omitted, analyzes all machines.
    
    region (optional):
        Grid region/mix for emission factor. Options:
        - US_Average (default): 0.385 kg CO2/kWh
        - Coal_Heavy: 0.95 kg CO2/kWh
        - Natural_Gas: 0.50 kg CO2/kWh
        - Renewable_Heavy: 0.10 kg CO2/kWh
        - UK: 0.20 kg CO2/kWh
        - France: 0.06 kg CO2/kWh
    
    Formula Used:
    ============
    Daily CO2 (kg) = Daily Energy (kWh) × Emission Factor (kg CO2/kWh)
    
    Example with US Average (0.385 kg CO2/kWh):
        100 kWh × 0.385 = 38.5 kg CO2
    
    Returns:
    --------
    JSON response with:
    - Daily carbon breakdown
    - Monthly totals (kg and tonnes)
    - Equivalent activities (car miles, trees needed)
    - Key insights and recommendations
    
    HTTP Status Codes:
    - 200: Successfully calculated carbon footprint
    - 404: No energy data found for specified filter
    - 500: Server error during calculation
    """
    
    try:
        # ====================================================================
        # Step 1: Query energy data from database
        # ====================================================================
        # Build the query - filter by machine_id if provided
        query = db.query(EnergyReading)
        
        if machine_id:
            query = query.filter(EnergyReading.machine_id == machine_id)
        
        # Execute query and get all matching records
        energy_readings = query.all()
        
        # ====================================================================
        # Step 2: Validate that data exists
        # ====================================================================
        # Return 404 if no data found
        if not energy_readings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No energy data found for the specified filter"
            )
        
        # ====================================================================
        # Step 3: Convert database objects to DataFrame
        # ====================================================================
        # Extract data from SQLAlchemy objects into dictionaries
        data_for_dataframe = [
            {
                'timestamp': reading.timestamp,
                'machine_id': reading.machine_id,
                'power_kw': reading.power_kw,
                'energy_consumed_kwh': reading.energy_consumed_kwh
            }
            for reading in energy_readings
        ]
        
        # Create a Pandas DataFrame from the list of dictionaries
        df = pd.DataFrame(data_for_dataframe)
        
        # ====================================================================
        # Step 4: Calculate carbon footprint using carbon_footprint module
        # ====================================================================
        # This function returns comprehensive carbon analysis
        carbon_report = calculate_co2_with_breakdown(
            df,
            energy_column='energy_consumed_kwh',
            region=region
        )
        
        # ====================================================================
        # Step 5: Format response for JSON output
        # ====================================================================
        # Build the API response
        response = {
            'analysis_date': datetime.now().isoformat(),
            'machine_id': machine_id or 'All Machines',
            'region': region,
            
            # Summary statistics
            'summary': {
                'total_energy_kwh': carbon_report['summary']['total_energy_kwh'],
                'emission_factor_kg_per_kwh': carbon_report['summary']['emission_factor_kg_per_kwh'],
                'monthly_co2_kg': carbon_report['summary']['monthly_co2_kg'],
                'monthly_co2_tonnes': carbon_report['summary']['monthly_co2_tonnes'],
                'daily_average_co2_kg': carbon_report['summary']['daily_average_co2_kg'],
                'daily_min_co2_kg': carbon_report['summary']['daily_min_co2_kg'],
                'daily_max_co2_kg': carbon_report['summary']['daily_max_co2_kg'],
            },
            
            # Daily breakdown - showing CO2 for each day
            'daily_breakdown': carbon_report['daily_breakdown'],
            
            # Real-world equivalencies to make numbers meaningful
            'equivalencies': {
                'car_miles_equivalent': carbon_report['equivalencies']['car_miles_equivalent'],
                'trees_needed_per_year': carbon_report['equivalencies']['trees_needed_per_year'],
                'car_months_equivalent': carbon_report['equivalencies']['car_months_equivalent'],
                'description': {
                    'car_miles_equivalent': 'Equivalent miles of car driving',
                    'trees_needed_per_year': 'Trees needed to offset yearly emissions at this rate',
                    'car_months_equivalent': 'Months of average car emissions'
                }
            },
            
            # Insights from the data
            'insights': carbon_report['insights']
        }
        
        return response
    
    # ========================================================================
    # ERROR HANDLING
    # ========================================================================
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating carbon footprint: {str(e)}"
        )

# ============================================================================
# Sustainability - Carbon Emissions Endpoint (Beginner-Friendly)
# ============================================================================
# A simplified version of the carbon analytics endpoint
# Perfect for beginners - clear structure and straightforward response

@app.get(
    "/sustainability/carbon",
    summary="Carbon Emissions Analysis",
    description="Calculate CO2 emissions from energy consumption. Simple and beginner-friendly endpoint."
)
def get_sustainability_carbon(
    machine_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Calculate CO2 emissions from energy consumption data.
    
    This is a beginner-friendly endpoint that shows:
    - Total CO2 emissions
    - Average daily emissions
    - Simple comparison (car miles equivalent)
    
    How it works:
    1. Fetch energy data from database (all machines or specific machine)
    2. Calculate CO2 using standard factor (0.385 kg CO2/kWh for US)
    3. Return simple, easy-to-understand results
    
    Parameters:
    -----------
    machine_id (optional):
        - If provided: analyze only this machine
        - If omitted: analyze all machines combined
        - Example: "PUMP-01", "COMPRESSOR-02"
    
    Returns:
    --------
    A JSON response with:
    - emissions: Total CO2 in kg and tonnes
    - daily_average: Average per day
    - energy_used: Total kWh consumed
    - car_miles_equivalent: How many miles of driving this equals
    - last_reading_date: When the data was collected
    
    Example Response (200 OK):
    {
      "status": "success",
      "emissions": {
        "total_kg_co2": 4812.5,
        "total_tonnes_co2": 4.81
      },
      "energy": {
        "total_kwh": 12500,
        "daily_average_kwh": 172.6
      },
      "equivalencies": {
        "car_miles": 11726
      },
      "data_points": 73,
      "last_reading_date": "2026-01-26"
    }
    
    Error Responses:
    - 404: No energy data found
    - 500: Server error during calculation
    """
    
    try:
        # ====================================================================
        # STEP 1: Create database tables if needed
        # ====================================================================
        # On first run, SQLAlchemy creates the energy_readings table
        Base.metadata.create_all(bind=engine)
        
        # ====================================================================
        # STEP 2: Query energy data from database
        # ====================================================================
        # Build the query to get energy readings
        query = db.query(EnergyReading)
        
        # If machine_id is provided, filter to that machine only
        if machine_id:
            query = query.filter(EnergyReading.machine_id == machine_id)
        
        # Execute query and fetch all results
        energy_readings = query.all()
        
        # ====================================================================
        # STEP 3: Validate that data exists
        # ====================================================================
        # If no data found, return 404 Not Found error
        if not energy_readings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No energy data found{' for machine ' + machine_id if machine_id else ''}"
            )
        
        # ====================================================================
        # STEP 4: Convert database results to Pandas DataFrame
        # ====================================================================
        # Extract data from SQLAlchemy objects into a list of dictionaries
        data_list = [
            {
                'timestamp': reading.timestamp,
                'energy_consumed_kwh': reading.energy_consumed_kwh
            }
            for reading in energy_readings
        ]
        
        # Create a Pandas DataFrame for easier calculation
        df = pd.DataFrame(data_list)
        
        # ====================================================================
        # STEP 5: Calculate CO2 emissions (US Average: 0.385 kg CO2/kWh)
        # ====================================================================
        
        # Emission factor = how much CO2 is released per kWh in the US
        # This is the average across all US electricity sources (coal, gas, renewables)
        emission_factor_kg_per_kwh = 0.385
        
        # Total energy consumed (sum all readings)
        total_energy_kwh = df['energy_consumed_kwh'].sum()
        
        # Calculate total CO2 emissions using the formula:
        # CO2 (kg) = Energy (kWh) × Emission Factor (kg CO2/kWh)
        total_co2_kg = total_energy_kwh * emission_factor_kg_per_kwh
        
        # Convert to tonnes (1 tonne = 1000 kg)
        total_co2_tonnes = total_co2_kg / 1000
        
        # ====================================================================
        # STEP 6: Calculate daily average
        # ====================================================================
        
        # Group data by date and sum energy per day
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_energy = df.groupby('date')['energy_consumed_kwh'].sum()
        
        # Calculate average daily energy and CO2
        daily_average_kwh = daily_energy.mean()
        daily_average_co2_kg = daily_average_kwh * emission_factor_kg_per_kwh
        
        # ====================================================================
        # STEP 7: Calculate equivalencies (make numbers meaningful)
        # ====================================================================
        
        # Car driving equivalency:
        # Average car emits 0.41 kg CO2 per km (or 0.66 kg per mile)
        # Formula: CO2 total / 0.41 kg per km = equivalent km
        # Then convert to miles for US audience
        car_miles_equivalent = (total_co2_kg / 0.41) * 0.621371  # km to miles conversion
        
        # ====================================================================
        # STEP 8: Get the date of the last reading
        # ====================================================================
        last_reading_date = pd.to_datetime(
            energy_readings[-1].timestamp
        ).strftime('%Y-%m-%d')
        
        # ====================================================================
        # STEP 9: Build and return the response
        # ====================================================================
        
        response = {
            # Success status indicator
            'status': 'success',
            
            # Main emissions data
            'emissions': {
                'total_kg_co2': round(total_co2_kg, 2),
                'total_tonnes_co2': round(total_co2_tonnes, 2),
                'emission_factor_used': f"{emission_factor_kg_per_kwh} kg CO2/kWh (US Average)"
            },
            
            # Energy consumption data
            'energy': {
                'total_kwh': round(total_energy_kwh, 2),
                'daily_average_kwh': round(daily_average_kwh, 2),
                'daily_average_co2_kg': round(daily_average_co2_kg, 2)
            },
            
            # Real-world equivalencies to understand the impact
            'equivalencies': {
                'car_miles': round(car_miles_equivalent, 0),
                'description': 'Equivalent miles of car driving at US average (0.41 kg CO2/km)'
            },
            
            # Metadata about the analysis
            'metadata': {
                'data_points': len(energy_readings),
                'days_analyzed': len(daily_energy),
                'last_reading_date': last_reading_date,
                'machine_id': machine_id or 'All Machines',
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
        
        return response
    
    # ========================================================================
    # ERROR HANDLING
    # ========================================================================
    
    except HTTPException:
        # Re-raise HTTP exceptions (like 404 Not Found)
        raise
    
    except Exception as e:
        # Handle any unexpected errors
        # In production, these would be logged for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating carbon emissions: {str(e)}"
        )


# ============================================================================
# Energy Prediction Endpoints
# ============================================================================
# Endpoints for predicting future energy consumption using Linear Regression

# Global prediction model (cached)
prediction_model = None
model_is_trained = False


@app.post("/prediction/train")
def train_prediction_model(db: Session = Depends(get_db)):
    """
    Train the Linear Regression energy prediction model.
    
    This endpoint:
    1. Queries all historical energy data from the database
    2. Trains a Linear Regression model on time-based features
    3. Returns training metrics and model status
    
    The model learns patterns like:
    - Higher consumption in afternoons (peak hours)
    - Lower consumption at night
    - Weekday vs weekend differences
    - Seasonal variations
    
    Requires:
    - At least 100 records in database for reliable training
    
    Returns:
        dict: Training status and accuracy metrics
    
    Example Response:
        {
            'status': 'success',
            'message': 'Model trained on 1234 records',
            'is_trained': True,
            'r2_score': 0.8342,
            'mae': 2.31,
            'rmse': 3.45
        }
    """
    global prediction_model, model_is_trained
    
    try:
        # ====================================================================
        # Step 1: Query historical energy data
        # ====================================================================
        Base.metadata.create_all(bind=engine)
        energy_readings = db.query(EnergyReading).all()
        
        if len(energy_readings) < 100:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data. Need 100+ records, have {len(energy_readings)}"
            )
        
        # Convert to DataFrame format
        data_list = []
        for reading in energy_readings:
            data_list.append({
                'timestamp': reading.timestamp,
                'energy_consumed_kwh': reading.energy_consumed_kwh
            })
        
        df = pd.DataFrame(data_list)
        
        # ====================================================================
        # Step 2: Initialize and train model
        # ====================================================================
        prediction_model = EnergyConsumptionPredictor()
        metrics = prediction_model.train(df)
        model_is_trained = True
        
        return {
            'status': 'success',
            'message': f'Model trained on {len(df)} records',
            'is_trained': True,
            'r2_score': float(metrics['r2_score']),
            'mae': float(metrics['mae']),
            'rmse': float(metrics['rmse']),
            'training_timestamp': datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Training failed: {str(e)}"
        )


@app.get("/prediction/next-7-days")
def predict_next_seven_days():
    """
    Predict energy consumption for the next 7 days (hourly).
    
    This is the main prediction endpoint that:
    1. Checks if the model is trained
    2. Generates hourly predictions for next 7 days
    3. Organizes results by day with summaries
    4. Returns clean, readable JSON
    
    The model uses Linear Regression with 6 time-based features:
    - Hour of day (0-23)
    - Day of week (Monday-Sunday)
    - Day of month (1-31)
    - Month (1-12)
    - Is weekend (yes/no)
    - Is business hours (9am-5pm)
    
    Returns:
        dict: 7-day forecast with hourly and daily summaries
    
    Example Response:
        {
            'status': 'success',
            'forecast_days': 7,
            'total_forecast_kwh': 5945.8,
            'daily_summary': [
                {
                    'date': '2026-01-27',
                    'day_name': 'Monday',
                    'total_kwh': 842.5,
                    'average_kwh': 35.1,
                    'peak_kwh': 52.3,
                    'peak_hour': 14,
                    'low_kwh': 18.2,
                    'low_hour': 3
                },
                ...
            ]
        }
    """
    global prediction_model, model_is_trained
    
    try:
        # ====================================================================
        # Step 1: Validate model is trained
        # ====================================================================
        if not model_is_trained or prediction_model is None:
            raise HTTPException(
                status_code=400,
                detail="Model not trained. Call POST /prediction/train first"
            )
        
        # ====================================================================
        # Step 2: Generate forecast for next 7 days
        # ====================================================================
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        
        # Get hourly predictions
        forecast_df = prediction_model.predict_range(
            start_date=start_date,
            end_date=end_date,
            frequency='H'  # Hourly predictions
        )
        
        # ====================================================================
        # Step 3: Organize by day with summaries
        # ====================================================================
        daily_summary = []
        
        for day_num in range(7):
            day = start_date + timedelta(days=day_num)
            day_data = forecast_df[
                (forecast_df['timestamp'].dt.date == day.date())
            ]
            
            if len(day_data) > 0:
                daily_summary.append({
                    'date': day.strftime('%Y-%m-%d'),
                    'day_name': day.strftime('%A'),
                    'total_kwh': float(round(day_data['predicted_energy_kwh'].sum(), 2)),
                    'average_kwh': float(round(day_data['predicted_energy_kwh'].mean(), 2)),
                    'peak_kwh': float(round(day_data['predicted_energy_kwh'].max(), 2)),
                    'peak_hour': int(day_data.loc[
                        day_data['predicted_energy_kwh'].idxmax(),
                        'timestamp'
                    ].hour),
                    'low_kwh': float(round(day_data['predicted_energy_kwh'].min(), 2)),
                    'low_hour': int(day_data.loc[
                        day_data['predicted_energy_kwh'].idxmin(),
                        'timestamp'
                    ].hour),
                    'hourly_count': len(day_data)
                })
        
        # ====================================================================
        # Step 4: Calculate overall statistics
        # ====================================================================
        total_kwh = float(round(forecast_df['predicted_energy_kwh'].sum(), 2))
        average_daily = float(round(total_kwh / 7, 2))
        
        # ====================================================================
        # Step 5: Return formatted response
        # ====================================================================
        return {
            'status': 'success',
            'forecast_days': 7,
            'generated_at': datetime.now().isoformat(),
            'forecast_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'summary': {
                'total_kwh': total_kwh,
                'average_daily_kwh': average_daily,
                'peak_day': max(daily_summary, key=lambda x: x['total_kwh'])['date'],
                'peak_day_kwh': max(daily_summary, key=lambda x: x['total_kwh'])['total_kwh']
            },
            'daily_summary': daily_summary
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/prediction/status")
def get_prediction_status():
    """
    Check if the prediction model is trained and ready.
    
    This is a quick status check endpoint that shows:
    - Whether the model has been trained
    - Number of features used
    - Model type
    
    Returns:
        dict: Model status information
    
    Example Response:
        {
            'is_trained': True,
            'model_type': 'Linear Regression',
            'features': 6,
            'message': 'Model ready for predictions'
        }
    """
    global model_is_trained, prediction_model
    
    if not model_is_trained or prediction_model is None:
        return {
            'is_trained': False,
            'model_type': 'Linear Regression',
            'features': 6,
            'message': 'Model not trained. Call POST /prediction/train first'
        }
    
    return {
        'is_trained': True,
        'model_type': 'Linear Regression',
        'features': len(prediction_model.feature_names),
        'feature_names': prediction_model.feature_names,
        'message': 'Model ready for predictions'
    }

# ============================================================================
# Run the Application
# ============================================================================
# This section only runs if the file is executed directly (not imported)
if __name__ == "__main__":
    # Import uvicorn - the ASGI server that runs FastAPI
    import uvicorn
    
    # Start the server on localhost:8000
    # - host="127.0.0.1": Only accessible from your local machine
    # - port=8000: Default FastAPI port
    # - reload=True: Auto-restart server when code changes (great for development)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
