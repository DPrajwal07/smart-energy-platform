# Sustainability Carbon Endpoint - Implementation Complete

## What Was Added

A new **beginner-friendly** FastAPI endpoint has been added to calculate CO2 emissions:

```
GET /sustainability/carbon
```

## Quick Reference

### Endpoint URL
```
http://127.0.0.1:8000/sustainability/carbon
```

### Parameters
```
machine_id (optional) - Filter to specific machine
  Example: ?machine_id=PUMP-01
```

### Formula
```
CO2 (kg) = Energy (kWh) × 0.385 kg CO2/kWh
```

## Example Usage

### cURL - All Machines
```bash
curl http://127.0.0.1:8000/sustainability/carbon
```

### cURL - Specific Machine
```bash
curl "http://127.0.0.1:8000/sustainability/carbon?machine_id=PUMP-01"
```

### Python
```python
import requests

response = requests.get('http://127.0.0.1:8000/sustainability/carbon')
data = response.json()

print(f"Total CO2: {data['emissions']['total_tonnes_co2']} tonnes")
print(f"Car miles equivalent: {data['equivalencies']['car_miles']:.0f} miles")
```

## Example Response

```json
{
  "status": "success",
  
  "emissions": {
    "total_kg_co2": 4812.5,
    "total_tonnes_co2": 4.81,
    "emission_factor_used": "0.385 kg CO2/kWh (US Average)"
  },
  
  "energy": {
    "total_kwh": 12500,
    "daily_average_kwh": 172.6,
    "daily_average_co2_kg": 66.5
  },
  
  "equivalencies": {
    "car_miles": 11726,
    "description": "Equivalent miles of car driving"
  },
  
  "metadata": {
    "data_points": 73,
    "days_analyzed": 30,
    "last_reading_date": "2026-01-26",
    "machine_id": "PUMP-01",
    "analysis_timestamp": "2026-01-26T14:30:00.123456"
  }
}
```

## Response Fields Explained

### Emissions
- **total_kg_co2**: Total CO2 in kilograms
- **total_tonnes_co2**: Total CO2 in metric tonnes
- **emission_factor_used**: The grid emission factor (0.385 for US)

### Energy
- **total_kwh**: Total energy consumed from all readings
- **daily_average_kwh**: Average energy per day
- **daily_average_co2_kg**: Average CO2 per day

### Equivalencies
- **car_miles**: How many miles of car driving this CO2 equals
- **description**: What the equivalency means

### Metadata
- **data_points**: Number of energy readings analyzed
- **days_analyzed**: Number of unique days
- **last_reading_date**: When the most recent data is from
- **machine_id**: Which machine analyzed (or "All Machines")
- **analysis_timestamp**: When this analysis was run

## Key Characteristics

✅ **Beginner-Friendly**
- Simple, easy-to-understand structure
- Clear variable names
- Straightforward formula

✅ **Well-Commented Code**
- 100+ lines of comments in implementation
- Step-by-step process explained
- Clear section headers

✅ **Structured JSON Response**
- Organized into logical sections
- Easy to parse and display
- Includes descriptive metadata

✅ **Error Handling**
- 404: No data found
- 500: Server error
- Clear error messages

✅ **Production Ready**
- Proper HTTP status codes
- Input validation
- Error handling
- Database integration

## Where It's Implemented

**File:** `main.py` (lines ~475-670)

**Function:** `get_sustainability_carbon()`

**Framework:** FastAPI

## How to Test

### Test 1: View in Swagger UI
```
http://127.0.0.1:8000/docs
```
Look for "/sustainability/carbon" endpoint

### Test 2: Call with Sample Data
```bash
# First, add energy data
curl -X POST http://127.0.0.1:8000/energy/add \
  -H "Content-Type: application/json" \
  -d '{"machine_id":"TEST","power_kw":50,"energy_consumed_kwh":100}'

# Then get carbon footprint
curl http://127.0.0.1:8000/sustainability/carbon?machine_id=TEST
```

Expected: ~38.5 kg CO2 (100 kWh × 0.385)

### Test 3: Multiple Machines
```bash
# Get all machines
curl http://127.0.0.1:8000/sustainability/carbon
```

## Code Implementation Details

### Step-by-Step Process
1. Create database tables
2. Query energy readings (with optional machine filter)
3. Validate data exists
4. Convert to Pandas DataFrame
5. Calculate total CO2 (Energy × 0.385)
6. Calculate daily averages
7. Calculate car miles equivalency
8. Build structured response
9. Return JSON

### Error Cases Handled
- **No data found** → 404 Not Found
- **Database error** → 500 Internal Server Error
- **Unexpected error** → 500 Internal Server Error

## Integration with Existing Code

✅ Uses existing `EnergyReading` model
✅ Uses existing database connection
✅ No schema changes needed
✅ Compatible with all other endpoints
✅ Follows same code style as other endpoints

## Comparison with /analytics/carbon

| Feature | /sustainability/carbon | /analytics/carbon |
|---------|----------------------|-------------------|
| **Complexity** | Beginner ✓ | Advanced |
| **Response size** | Small | Large |
| **Regional support** | US only | 8 regions |
| **Daily breakdown** | No | Yes |
| **Insights** | No | Yes |
| **For beginners** | ✓ | No |
| **For analysis** | No | ✓ |

## Documentation

See **SUSTAINABILITY_CARBON_GUIDE.md** for:
- Complete API documentation
- More code examples
- Troubleshooting
- Integration tips
- Common questions

## Status

🟢 **Production Ready**

- ✅ Implemented
- ✅ Commented
- ✅ Error handling
- ✅ Tested
- ✅ Documented

---

**Endpoint:** `/sustainability/carbon`
**Method:** GET
**Status Code:** 200 (success), 404 (no data), 500 (error)
**Response Format:** JSON
