# Smart Energy Platform API

A simple FastAPI backend for monitoring and storing industrial energy consumption data.

## Features

- ✅ REST API endpoints for energy data management
- ✅ PostgreSQL database integration with SQLAlchemy ORM
- ✅ JSON request/response validation with Pydantic
- ✅ Error handling with proper HTTP status codes
- ✅ Interactive API documentation (Swagger UI)
- ✅ Beginner-friendly code with detailed comments

## Installation

### Prerequisites
- Python 3.7+
- PostgreSQL server

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure database** (edit `database.py`):
```python
DATABASE_URL = "postgresql://username:password@localhost:5432/smart_energy"
```

3. **Create PostgreSQL database:**
```bash
createdb smart_energy
```

## Running the Application

```bash
python main.py
```

The API will start at: `http://127.0.0.1:8000`

## API Endpoints

### 1. Root Endpoint
```
GET /
```
Welcome message with API information.

**Response:**
```json
{
  "message": "Welcome to Smart Energy Platform API",
  "description": "Monitor and optimize your energy usage",
  "timestamp": "2026-01-26T10:30:00.123456",
  "version": "1.0.0"
}
```

### 2. Health Check
```
GET /health
```
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-26T10:30:00.123456"
}
```

### 3. Sample Energy Data
```
GET /energy/sample
```
Returns sample industrial energy data.

**Response:**
```json
{
  "machine_id": "MACHINE-001",
  "power_kw": 45.5,
  "energy_consumed_kwh": 1250.75,
  "timestamp": "2026-01-26T10:30:00.123456"
}
```

### 4. Add Energy Reading (JSON) ⭐ NEW
```
POST /energy/add
Content-Type: application/json
```

Add a new energy reading to the database using JSON.

**Request Body:**
```json
{
  "machine_id": "MACHINE-001",
  "power_kw": 45.5,
  "energy_consumed_kwh": 1250.75
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "machine_id": "MACHINE-001",
  "power_kw": 45.5,
  "energy_consumed_kwh": 1250.75,
  "timestamp": "2026-01-26T10:30:00.123456"
}
```

**Using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/energy/add" \
  -H "Content-Type: application/json" \
  -d '{
    "machine_id": "MACHINE-001",
    "power_kw": 45.5,
    "energy_consumed_kwh": 1250.75
  }'
```

**Using Python requests:**
```python
import requests

url = "http://127.0.0.1:8000/energy/add"
data = {
    "machine_id": "MACHINE-001",
    "power_kw": 45.5,
    "energy_consumed_kwh": 1250.75
}

response = requests.post(url, json=data)
print(response.json())
```

### 5. Get All Energy Readings
```
GET /energy/readings
```
Retrieve all energy readings from the database.

**Response:**
```json
[
  {
    "id": 1,
    "machine_id": "MACHINE-001",
    "power_kw": 45.5,
    "energy_consumed_kwh": 1250.75,
    "timestamp": "2026-01-26T10:30:00.123456"
  }
]
```

### 6. Add Energy Reading (Query Parameters)
```
POST /energy/readings?machine_id=MACHINE-001&power_kw=45.5&energy_consumed_kwh=1250.75
```

Alternative endpoint using query parameters.

### 7. Daily Energy Analytics ⭐ NEW
```
GET /analytics/daily
GET /analytics/daily?machine_id=MACHINE-001
```

Analyze energy consumption data by day using Pandas.

**Request:**
```bash
# All machines
curl "http://127.0.0.1:8000/analytics/daily"

# Specific machine
curl "http://127.0.0.1:8000/analytics/daily?machine_id=MACHINE-001"
```

**Response (200 OK):**
```json
{
  "analysis_date": "2026-01-26T10:30:00.123456",
  "machine_id": "MACHINE-001",
  "data_points": 48,
  "daily_data": [
    {
      "date": "2026-01-01",
      "total_energy_kwh": 1250.75
    },
    {
      "date": "2026-01-02",
      "total_energy_kwh": 1340.20
    }
  ],
  "summary": {
    "average_daily_kwh": 1295.48,
    "min_daily_kwh": 1250.75,
    "max_daily_kwh": 1340.20,
    "total_days": 2
  }
}
```

**Using Python requests:**
```python
import requests

# Get analytics for all machines
response = requests.get("http://127.0.0.1:8000/analytics/daily")
data = response.json()

print(f"Average daily consumption: {data['summary']['average_daily_kwh']:.2f} kWh")
print(f"Total days analyzed: {data['summary']['total_days']}")

# Get analytics for specific machine
response = requests.get(
    "http://127.0.0.1:8000/analytics/daily",
    params={"machine_id": "MACHINE-001"}
)
```

### 8. Carbon Footprint Analysis ⭐ NEW
```
GET /analytics/carbon
GET /analytics/carbon?machine_id=PUMP-01&region=US_Average
```

Calculate CO2 emissions from energy consumption. Shows environmental impact with daily breakdown, monthly totals, and equivalencies (car miles, trees needed).

**Regional Emission Factors (kg CO2/kWh):**
- France: 0.06 (mostly nuclear)
- Renewable_Heavy: 0.10 (high renewable mix)
- UK: 0.20 (natural gas + renewables)
- **US_Average: 0.385** (default - mixed grid)
- Natural_Gas: 0.50 (natural gas dominant)
- Coal_Heavy: 0.95 (coal-heavy region)

**Formula Used:**
```
Daily CO2 (kg) = Daily Energy (kWh) × Emission Factor (kg CO2/kWh)
Monthly CO2 = Sum of all daily CO2 emissions
```

**Request:**
```bash
# All machines, US average
curl "http://127.0.0.1:8000/analytics/carbon"

# Specific machine, renewable region
curl "http://127.0.0.1:8000/analytics/carbon?machine_id=PUMP-01&region=Renewable_Heavy"
```

**Response (200 OK):**
```json
{
  "analysis_date": "2026-01-26T10:30:00.123456",
  "machine_id": "PUMP-01",
  "region": "US_Average",
  
  "summary": {
    "total_energy_kwh": 12500,
    "emission_factor_kg_per_kwh": 0.385,
    "monthly_co2_kg": 4812.5,
    "monthly_co2_tonnes": 4.8125,
    "daily_average_co2_kg": 172.6,
    "daily_min_co2_kg": 150.2,
    "daily_max_co2_kg": 195.8
  },
  
  "daily_breakdown": [
    {
      "date": "2026-01-01",
      "total_energy_kwh": 450,
      "co2_kg": 173.25
    }
  ],
  
  "equivalencies": {
    "car_miles_equivalent": 11726,
    "trees_needed_per_year": 289,
    "car_months_equivalent": 12.5
  },
  
  "insights": {
    "observations": ["High monthly emissions: 4.8 tonnes CO2"],
    "recommendations": [
      "Consider energy efficiency improvements",
      "Explore renewable energy options"
    ]
  }
}
```

**Using Python requests:**
```python
import requests

# Get carbon footprint analysis
response = requests.get("http://127.0.0.1:8000/analytics/carbon")
data = response.json()

summary = data['summary']
print(f"Monthly CO2: {summary['monthly_co2_tonnes']:.2f} tonnes")
print(f"Daily average: {summary['daily_average_co2_kg']:.1f} kg CO2/day")

equiv = data['equivalencies']
print(f"Equivalent to {equiv['car_miles_equivalent']:.0f} miles of driving")
print(f"Needs {equiv['trees_needed_per_year']:.0f} trees/year to offset")

# View recommendations
for rec in data['insights']['recommendations']:
    print(f"→ {rec}")
```

**Note:** For a simpler, beginner-friendly version, use `/sustainability/carbon` instead.

## Interactive API Documentation

After starting the server, visit:

- **Swagger UI** (Recommended): `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

These provide interactive documentation where you can test endpoints directly.

## Project Structure

```
Smart Energy Platform/
├── main.py                    # Main FastAPI application with all endpoints
├── database.py                # Database configuration and session management
├── models.py                  # SQLAlchemy database models (EnergyReading)
├── schemas.py                 # Pydantic data validation models
├── analysis.py                # Energy data analysis functions (Pandas)
├── carbon_footprint.py        # Carbon footprint calculation module (NEW)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── CARBON_FOOTPRINT_GUIDE.md  # Detailed carbon calculation guide (NEW)
├── CARBON_IMPLEMENTATION.md   # Implementation summary (NEW)
└── test_carbon_footprint.py  # Carbon module test suite (NEW)
```

## Error Handling

The `/energy/add` endpoint includes error handling:

- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: Database operation failed

Example error response:
```json
{
  "detail": "Failed to save energy reading to database"
}
```

## Input Validation

The `/energy/add` endpoint validates all inputs:

- `machine_id`: Must be 1-50 characters
- `power_kw`: Must be >= 0
- `energy_consumed_kwh`: Must be >= 0

Invalid inputs will return a 422 Unprocessable Entity error with details.

## Database Schema

**energy_readings table:**

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO-INCREMENT |
| machine_id | VARCHAR(50) | NOT NULL, INDEXED |
| power_kw | FLOAT | NOT NULL, >= 0 |
| energy_consumed_kwh | FLOAT | NOT NULL, >= 0 |
| timestamp | DATETIME | NOT NULL, DEFAULT NOW(), INDEXED |

## Development Notes

- Auto-reload is enabled: changes to `.py` files automatically restart the server
- Database tables are created automatically on first API call
- All code includes detailed comments for learning

## Next Steps

- Add authentication (JWT tokens)
- Create user accounts and machine assignments
- Add data aggregation endpoints (daily/monthly summaries)
- Implement data export (CSV, PDF)
- Add alerting for high power consumption
- Deploy to production (Docker, cloud hosting)

## License

MIT License

---

**Created for Smart Energy Platform** | January 2026
