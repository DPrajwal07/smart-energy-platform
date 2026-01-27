# /analytics/daily Endpoint Guide

## Overview

The `/analytics/daily` endpoint analyzes energy consumption data stored in PostgreSQL and returns daily aggregated statistics using Pandas.

## Endpoint Details

**HTTP Method:** GET  
**Path:** `/analytics/daily`  
**Parameters:** Optional `machine_id` query parameter  
**Status Code:** 200 OK (success) or 404 Not Found (no data)

## How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Client Request                                        │
│               GET /analytics/daily?machine_id=MACHINE-001               │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FastAPI Endpoint                                      │
│              get_daily_analytics(machine_id, db)                        │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Step 1: Query Database                               │
│         db.query(EnergyReading).filter(...).all()                       │
│         Fetch readings from PostgreSQL                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Step 2: Convert to DataFrame                         │
│         [EnergyReading objects] → pandas.DataFrame                      │
│         Transform SQLAlchemy models to tabular data                     │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Step 3: Analyze Data                                 │
│         calculate_daily_consumption(df)                                 │
│         Group by date, sum energy_consumed_kwh                          │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Step 4: Calculate Statistics                         │
│         mean, min, max of daily consumption                             │
│         Count total days                                                │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Step 5: Format Response                              │
│         Convert DataFrame to JSON-serializable dictionaries             │
│         Build response object with metadata                             │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    JSON Response                                         │
│         {                                                                │
│           "analysis_date": "2026-01-26T10:30:00",                       │
│           "machine_id": "MACHINE-001",                                  │
│           "data_points": 48,                                            │
│           "daily_data": [...],                                          │
│           "summary": {...}                                              │
│         }                                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

## Usage Examples

### Example 1: Get Analytics for All Machines

```bash
curl "http://127.0.0.1:8000/analytics/daily"
```

**Response:**
```json
{
  "analysis_date": "2026-01-26T10:30:00.123456",
  "machine_id": "All Machines",
  "data_points": 96,
  "daily_data": [
    {"date": "2026-01-01", "total_energy_kwh": 2234.95},
    {"date": "2026-01-02", "total_energy_kwh": 2390.50}
  ],
  "summary": {
    "average_daily_kwh": 2312.73,
    "min_daily_kwh": 2234.95,
    "max_daily_kwh": 2390.50,
    "total_days": 2
  }
}
```

### Example 2: Get Analytics for Specific Machine

```bash
curl "http://127.0.0.1:8000/analytics/daily?machine_id=MACHINE-001"
```

**Response:**
```json
{
  "analysis_date": "2026-01-26T10:30:00.123456",
  "machine_id": "MACHINE-001",
  "data_points": 48,
  "daily_data": [
    {"date": "2026-01-01", "total_energy_kwh": 1250.75},
    {"date": "2026-01-02", "total_energy_kwh": 1340.20}
  ],
  "summary": {
    "average_daily_kwh": 1295.48,
    "min_daily_kwh": 1250.75,
    "max_daily_kwh": 1340.20,
    "total_days": 2
  }
}
```

### Example 3: Python with Requests

```python
import requests
import json

# Get analytics for specific machine
response = requests.get(
    "http://127.0.0.1:8000/analytics/daily",
    params={"machine_id": "MACHINE-001"}
)

if response.status_code == 200:
    data = response.json()
    
    # Print summary
    summary = data['summary']
    print(f"Machine: {data['machine_id']}")
    print(f"Average daily consumption: {summary['average_daily_kwh']:.2f} kWh")
    print(f"Range: {summary['min_daily_kwh']:.2f} - {summary['max_daily_kwh']:.2f} kWh")
    
    # Print daily breakdown
    print("\nDaily Breakdown:")
    for day in data['daily_data']:
        print(f"  {day['date']}: {day['total_energy_kwh']:.2f} kWh")

elif response.status_code == 404:
    print("No data found for this machine")
```

### Example 4: JavaScript/Node.js

```javascript
// Using fetch API
const response = await fetch(
  'http://127.0.0.1:8000/analytics/daily?machine_id=MACHINE-001'
);

if (response.ok) {
  const data = await response.json();
  
  console.log(`Machine: ${data.machine_id}`);
  console.log(`Average: ${data.summary.average_daily_kwh.toFixed(2)} kWh/day`);
  
  data.daily_data.forEach(day => {
    console.log(`${day.date}: ${day.total_energy_kwh.toFixed(2)} kWh`);
  });
} else {
  console.error('No data found');
}
```

## Response Fields

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `analysis_date` | string (ISO 8601) | When the analysis was performed |
| `machine_id` | string | Which machine(s) were analyzed |
| `data_points` | integer | Number of readings processed |
| `daily_data` | array | List of daily totals |
| `summary` | object | Statistics about the data |

### Daily Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `date` | string (YYYY-MM-DD) | The date |
| `total_energy_kwh` | number | Total energy consumed that day (kWh) |

### Summary Fields

| Field | Type | Description |
|-------|------|-------------|
| `average_daily_kwh` | number | Mean daily consumption |
| `min_daily_kwh` | number | Lowest daily consumption |
| `max_daily_kwh` | number | Highest daily consumption |
| `total_days` | integer | Number of days analyzed |

## Error Handling

### 404 Not Found
Occurs when no energy data exists for the requested machine.

```json
{
  "detail": "No energy data found for machine MACHINE-999"
}
```

### 500 Internal Server Error
Occurs if there's a database or processing error.

```json
{
  "detail": "Error analyzing energy data: Database connection failed"
}
```

## Code Implementation Details

### Variable Names (Clear and Self-Documenting)

```python
# Database query variables
energy_readings = query.all()  # Clear: contains EnergyReading objects

# Data transformation
data_for_dataframe = [...]  # Clear: preparing data for Pandas
df = pd.DataFrame(...)      # Standard Pandas convention

# Analysis results
daily_consumption = calculate_daily_consumption(df)
summary_stats = {...}       # Clear: dictionary of statistics

# Response building
daily_data = [...]          # Clear: the daily breakdown list
response = {...}            # Clear: the API response object
```

### Comments Explain "Why" Not "What"

```python
# GOOD - Explains the business logic
if machine_id:
    # Filter to specific machine for more targeted analysis
    query = query.filter(EnergyReading.machine_id == machine_id)

# GOOD - Explains the technical approach
# Transform SQLAlchemy objects into a dictionary for Pandas
# Pandas needs standard Python types, not SQLAlchemy models
data_for_dataframe = [...]
```

## Testing the Endpoint

### Using the Provided Test Script

```bash
python test_analytics.py
```

This script will:
1. Check if data exists
2. Add sample data if needed
3. Test the endpoint
4. Display formatted results

### Manual Testing with Swagger UI

1. Start the server: `python main.py`
2. Open browser: `http://127.0.0.1:8000/docs`
3. Find the `/analytics/daily` endpoint
4. Click "Try it out"
5. Optionally enter machine_id parameter
6. Click "Execute"

## Performance Considerations

- **Query Time**: O(n) where n = number of readings
  - For 1 year of hourly data (8,760 readings): ~100ms
  - For 5 years of data: ~500ms

- **Memory**: DataFrame uses ~1-2 MB per 10,000 readings
  
- **Optimization**: For large datasets, add date range filter:

```python
from datetime import datetime, timedelta

# Only analyze last 30 days
since = datetime.now() - timedelta(days=30)
query = query.filter(EnergyReading.timestamp >= since)
```

## Common Questions

**Q: Can I filter by date range?**  
A: Not yet, but you can add it! Modify the endpoint to accept `start_date` and `end_date` parameters.

**Q: Can I get hourly instead of daily?**  
A: Yes! Use `df['timestamp'].dt.strftime('%Y-%m-%d %H:00:00').groupby(...)` instead.

**Q: Can I export as CSV?**  
A: Yes! Return the CSV directly using FastAPI's FileResponse:
```python
from fastapi.responses import FileResponse
# Convert daily_consumption DataFrame to CSV
return FileResponse(path, filename="daily_consumption.csv")
```

---

Created for Smart Energy Platform | January 2026
