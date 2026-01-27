"""
FastAPI Integration for Energy Prediction Model

This module demonstrates how to integrate the Linear Regression model
into a FastAPI application with endpoints for training and prediction.

Endpoints:
- POST /prediction/train - Train the model with historical data
- GET /prediction/forecast/{days} - Get energy forecast
- POST /prediction/predict - Predict for a specific timestamp
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from energy_prediction_model import EnergyConsumptionPredictor
from database import get_db
from models import EnergyReading

# Create router for prediction endpoints
router = APIRouter(prefix="/prediction", tags=["Energy Prediction"])

# Global model instance (in production, store in database)
prediction_model = None


@router.post(
    "/train",
    summary="Train Energy Prediction Model",
    description="Train the Linear Regression model using historical energy data"
)
def train_prediction_model(db: Session = Depends(get_db)):
    """
    Train the energy consumption prediction model.
    
    The model learns patterns from historical data:
    - How consumption changes throughout the day
    - Weekday vs weekend patterns
    - Seasonal variations
    
    Steps:
    1. Query all energy readings from database
    2. Create predictor model
    3. Train on historical data
    4. Return training metrics
    
    Returns:
        dict: Training metrics (R², MAE, RMSE, coefficients)
        
    Raises:
        HTTPException(400): If insufficient data (need at least 100 records)
        HTTPException(500): If training fails
    """
    try:
        # ================================================================
        # Step 1: Query historical energy data from database
        # ================================================================
        energy_readings = db.query(EnergyReading).all()
        
        if len(energy_readings) < 100:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data for training. Need 100+ records, have {len(energy_readings)}"
            )
        
        # Convert to format the model expects
        # Create list of dictionaries
        data_list = []
        for reading in energy_readings:
            data_list.append({
                'timestamp': reading.timestamp,
                'energy_consumed_kwh': reading.energy_consumed_kwh
            })
        
        # Convert to pandas DataFrame
        import pandas as pd
        df = pd.DataFrame(data_list)
        
        # ================================================================
        # Step 2: Initialize the model
        # ================================================================
        global prediction_model
        prediction_model = EnergyConsumptionPredictor()
        
        # ================================================================
        # Step 3: Train the model
        # ================================================================
        metrics = prediction_model.train(df)
        
        # ================================================================
        # Step 4: Return results
        # ================================================================
        return {
            'status': 'success',
            'message': f'Model trained on {len(df)} records',
            'training_metrics': metrics,
            'is_model_ready': True,
            'timestamp': datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Training failed: {str(e)}"
        )


@router.get(
    "/forecast/{days}",
    summary="Get Energy Forecast",
    description="Get hourly energy consumption forecast for the next N days"
)
def get_forecast(
    days: int = Query(7, ge=1, le=30, description="Number of days to forecast (1-30)"),
    db: Session = Depends(get_db)
):
    """
    Get energy consumption forecast for the next N days (hourly).
    
    Process:
    1. Check if model is trained
    2. Generate hourly timestamps for requested period
    3. Predict energy for each timestamp
    4. Return as JSON with daily summaries
    
    Args:
        days (int): Number of days to forecast (1-30)
        
    Returns:
        dict: Hourly and daily forecast data
        
    Raises:
        HTTPException(400): If model not trained
    """
    try:
        # Validate model is trained
        if prediction_model is None or not prediction_model.is_trained:
            raise HTTPException(
                status_code=400,
                detail="Model not trained. Call POST /prediction/train first"
            )
        
        # ================================================================
        # Generate forecast
        # ================================================================
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days)
        
        # Get hourly predictions
        forecast_df = prediction_model.predict_range(
            start_date=start_date,
            end_date=end_date,
            frequency='H'
        )
        
        # ================================================================
        # Organize by day with summaries
        # ================================================================
        daily_summary = []
        
        for day_num in range(days):
            day = start_date + timedelta(days=day_num)
            day_data = forecast_df[
                (forecast_df['timestamp'].dt.date == day.date())
            ]
            
            if len(day_data) > 0:
                daily_summary.append({
                    'date': day.strftime('%Y-%m-%d'),
                    'day_name': day.strftime('%A'),
                    'total_kwh': float(day_data['predicted_energy_kwh'].sum()),
                    'average_kwh': float(day_data['predicted_energy_kwh'].mean()),
                    'peak_kwh': float(day_data['predicted_energy_kwh'].max()),
                    'peak_hour': int(day_data.loc[
                        day_data['predicted_energy_kwh'].idxmax(),
                        'timestamp'
                    ].hour),
                    'low_kwh': float(day_data['predicted_energy_kwh'].min()),
                    'low_hour': int(day_data.loc[
                        day_data['predicted_energy_kwh'].idxmin(),
                        'timestamp'
                    ].hour),
                    'hourly_count': len(day_data)
                })
        
        # ================================================================
        # Prepare response
        # ================================================================
        return {
            'status': 'success',
            'forecast_days': days,
            'generated_at': datetime.now().isoformat(),
            'forecast_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'daily_summary': daily_summary,
            'total_forecast_kwh': float(forecast_df['predicted_energy_kwh'].sum()),
            'average_daily_kwh': float(
                forecast_df['predicted_energy_kwh'].sum() / days
            )
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Forecast generation failed: {str(e)}"
        )


@router.post(
    "/predict",
    summary="Predict Energy for Specific Time",
    description="Predict energy consumption for a specific date and time"
)
def predict_energy(
    year: int = Query(..., ge=2024, le=2050),
    month: int = Query(..., ge=1, le=12),
    day: int = Query(..., ge=1, le=31),
    hour: int = Query(12, ge=0, le=23),
    minute: int = Query(0, ge=0, le=59),
    db: Session = Depends(get_db)
):
    """
    Predict energy consumption for a specific timestamp.
    
    Uses the trained Linear Regression model to estimate energy usage
    based on time features (hour, day of week, month, etc.)
    
    Args:
        year (int): Year for prediction
        month (int): Month (1-12)
        day (int): Day of month (1-31)
        hour (int): Hour of day (0-23)
        minute (int): Minute (0-59)
        
    Returns:
        dict: Prediction with features and calculation details
        
    Raises:
        HTTPException(400): If model not trained or invalid date
        HTTPException(500): If prediction fails
        
    Example:
        GET /prediction/predict?year=2026&month=1&day=28&hour=14&minute=0
    """
    try:
        # Validate model
        if prediction_model is None or not prediction_model.is_trained:
            raise HTTPException(
                status_code=400,
                detail="Model not trained. Call POST /prediction/train first"
            )
        
        # ================================================================
        # Create timestamp from parameters
        # ================================================================
        try:
            timestamp = datetime(year, month, day, hour, minute)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date/time: {str(e)}"
            )
        
        # ================================================================
        # Make prediction
        # ================================================================
        prediction = prediction_model.predict(timestamp)
        
        # ================================================================
        # Enhance response with additional context
        # ================================================================
        features = prediction['features']
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                     'Friday', 'Saturday', 'Sunday']
        month_names = ['', 'January', 'February', 'March', 'April', 'May',
                       'June', 'July', 'August', 'September', 'October',
                       'November', 'December']
        
        # Add human-readable features
        prediction['readable_time'] = {
            'date': timestamp.strftime('%A, %B %d, %Y'),
            'time': timestamp.strftime('%I:%M %p'),
            'is_weekend': bool(features['is_weekend']),
            'is_business_hour': bool(features['is_business_hour'])
        }
        
        # Add context about the prediction
        prediction['context'] = {
            'typical_daytime': 40,  # Example typical kWh
            'typical_nighttime': 15,  # Example typical kWh
            'prediction_above_average': prediction['predicted_energy_kwh'] > 30,
            'model_type': 'Linear Regression',
            'features_used': 6
        }
        
        return prediction
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get(
    "/model-status",
    summary="Get Model Status",
    description="Check if the prediction model is trained and ready"
)
def get_model_status():
    """
    Get the current status of the prediction model.
    
    Returns:
        dict: Model status and readiness information
        
    Example Response:
        {
            'is_trained': True,
            'model_type': 'Linear Regression',
            'features': ['hour', 'day_of_week', 'day_of_month', 'month', 'is_weekend', 'is_business_hour'],
            'message': 'Model ready for predictions'
        }
    """
    if prediction_model is None:
        return {
            'is_trained': False,
            'model_type': 'Linear Regression',
            'message': 'Model not yet initialized. Call POST /prediction/train to train.',
            'features': []
        }
    
    return {
        'is_trained': prediction_model.is_trained,
        'model_type': 'Linear Regression',
        'features': prediction_model.feature_names,
        'message': 'Model ready for predictions' if prediction_model.is_trained else 'Model initialized but not trained',
        'status': 'ready' if prediction_model.is_trained else 'pending_training'
    }


@router.get(
    "/explain",
    summary="Explain Model",
    description="Get a plain-language explanation of how the model makes predictions"
)
def explain_model():
    """
    Get a detailed explanation of how the trained model works.
    
    Returns:
        dict: Human-readable model explanation
        
    Raises:
        HTTPException(400): If model not trained
    """
    if prediction_model is None or not prediction_model.is_trained:
        raise HTTPException(
            status_code=400,
            detail="Model not trained. Call POST /prediction/train first"
        )
    
    explanation = prediction_model.explain_model()
    
    return {
        'status': 'success',
        'explanation': explanation,
        'model_type': 'Linear Regression',
        'features_count': len(prediction_model.feature_names),
        'features': prediction_model.feature_names,
        'coefficients': dict(zip(
            prediction_model.feature_names,
            prediction_model.model.coef_.tolist()
        )),
        'intercept': float(prediction_model.model.intercept_)
    }


# Export router for main app
__all__ = ['router', 'prediction_model']
