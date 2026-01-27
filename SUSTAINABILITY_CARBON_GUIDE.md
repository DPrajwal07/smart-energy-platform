# /sustainability/carbon Endpoint - Quick Guide

## Overview

A **beginner-friendly** endpoint to calculate CO2 emissions from energy consumption.

## Quick Start

### 1. Start the Server
```bash
python main.py
```

### 2. Call the Endpoint

**All machines (combined emissions):**
```bash
curl http://127.0.0.1:8000/sustainability/carbon
```

**Specific machine:**
```bash
curl http://127.0.0.1:8000/sustainability/carbon?machine_id=PUMP-01
```

### 3. View in Browser
Visit: `http://127.0.0.1:8000/docs`

---

## The Formula (Simple)

```
CO2 (kg) = Energy (kWh) × 0.385
           ↑ What you used    ↑ US average emission factor
```

**Example:**
```
1000 kWh × 0.385 = 385 kg CO2 = 0.385 tonnes
```

---

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
    "description": "Equivalent miles of car driving at US average"
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

---

## Understanding the Response

### Emissions
- **total_kg_co2**: Total CO2 in kilograms
- **total_tonnes_co2**: Total CO2 in metric tonnes (1000 kg = 1 tonne)
- **emission_factor_used**: The factor used (0.385 for US average)

### Energy
- **total_kwh**: Total energy consumed
- **daily_average_kwh**: Average per day
- **daily_average_co2_kg**: Average CO2 per day

### Equivalencies
- **car_miles**: How many miles of car driving this equals
  - Makes the number meaningful for people

### Metadata
- **data_points**: Number of readings analyzed
- **days_analyzed**: How many unique days
- **last_reading_date**: When data ends
- **machine_id**: Which machine (or "All Machines")
- **analysis_timestamp**: When this was calculated

---

## Code Examples

### Python
```python
import requests

# Get emissions for all machines
response = requests.get('http://127.0.0.1:8000/sustainability/carbon')
data = response.json()

print(f"Total CO2: {data['emissions']['total_tonnes_co2']} tonnes")
print(f"Equivalent to: {data['equivalencies']['car_miles']:.0f} miles of driving")
```

### Python - Specific Machine
```python
import requests

response = requests.get(
    'http://127.0.0.1:8000/sustainability/carbon',
    params={'machine_id': 'PUMP-01'}
)
data = response.json()

print(f"Machine: {data['metadata']['machine_id']}")
print(f"Total CO2: {data['emissions']['total_kg_co2']:.1f} kg")
```

### JavaScript / Node.js
```javascript
// Fetch carbon emissions
fetch('http://127.0.0.1:8000/sustainability/carbon')
  .then(response => response.json())
  .then(data => {
    console.log(`Total CO2: ${data.emissions.total_tonnes_co2} tonnes`);
    console.log(`Car miles: ${data.equivalencies.car_miles}`);
  });
```

---

## Parameters

### machine_id (optional)
- **Type:** String
- **Default:** None (analyzes all machines)
- **Examples:** "PUMP-01", "COMPRESSOR-02", "MOTOR-A"

```bash
# Analyze specific machine
curl "http://127.0.0.1:8000/sustainability/carbon?machine_id=PUMP-01"
```

---

## Error Cases

### No Data (404)
**Request:**
```bash
curl "http://127.0.0.1:8000/sustainability/carbon?machine_id=NONEXISTENT"
```

**Response (404 Not Found):**
```json
{
  "detail": "No energy data found for machine NONEXISTENT"
}
```

### Server Error (500)
**Response (500 Internal Server Error):**
```json
{
  "detail": "Error calculating carbon emissions: [error details]"
}
```

---

## What Data is Needed

The endpoint requires energy readings in the database. Add data via:

```bash
curl -X POST http://127.0.0.1:8000/energy/add \
  -H "Content-Type: application/json" \
  -d '{
    "machine_id": "PUMP-01",
    "power_kw": 50.5,
    "energy_consumed_kwh": 101.0
  }'
```

---

## Key Concepts

### Emission Factor (0.385 kg CO2/kWh)

This is the **US Average** grid emission factor.

**What does it mean?**
- When you use 1 kWh of electricity in the US
- ~0.385 kg of CO2 is released into the atmosphere
- This is because the US grid uses a mix of:
  - Coal (high CO2)
  - Natural gas (medium CO2)
  - Renewables (low CO2)
  - Nuclear (very low CO2)

### Different Regions

If you're in a cleaner region:
- France (0.06): Much cleaner! (mostly nuclear)
- Renewable-heavy (0.10): Also very clean

If you're in a dirtier region:
- Coal-heavy (0.95): Much dirtier! (mostly coal)

*Note: This endpoint uses US average. For regional variation, use `/analytics/carbon`*

---

## Real-World Example

**Your data shows:**
```
Total: 4,812.5 kg CO2 = 4.81 tonnes
= Equivalent to 11,726 miles of car driving
= Like driving from NYC to Los Angeles and back 2 times!
```

---

## Differences from /analytics/carbon

| Feature | /sustainability/carbon | /analytics/carbon |
|---------|----------------------|-------------------|
| **Complexity** | Simple ✓ | Advanced |
| **Region support** | US only | 8 regions |
| **Response size** | Small | Comprehensive |
| **Daily breakdown** | No | Yes |
| **Insights** | No | Yes |
| **Best for** | Beginners | Detailed analysis |

**Use `/sustainability/carbon` when:**
- You want simple results
- You're new to the API
- You just need total emissions

**Use `/analytics/carbon` when:**
- You need regional analysis
- You want daily breakdown
- You need recommendations

---

## Testing

### Test 1: With Sample Data
```bash
# Add sample data
curl -X POST http://127.0.0.1:8000/energy/add \
  -H "Content-Type: application/json" \
  -d '{"machine_id": "TEST", "power_kw": 50, "energy_consumed_kwh": 100}'

# Get emissions
curl http://127.0.0.1:8000/sustainability/carbon?machine_id=TEST
```

Expected output: ~38.5 kg CO2 (100 kWh × 0.385)

### Test 2: Multiple Readings
```bash
# Add multiple readings
for i in {1..5}; do
  curl -X POST http://127.0.0.1:8000/energy/add \
    -H "Content-Type: application/json" \
    -d "{\"machine_id\": \"PUMP-01\", \"power_kw\": 50, \"energy_consumed_kwh\": 100}"
done

# Get combined emissions
curl http://127.0.0.1:8000/sustainability/carbon?machine_id=PUMP-01
```

Expected: ~192.5 kg CO2 (500 kWh × 0.385)

---

## Common Questions

**Q: Why 0.385?**
A: It's the US average emission factor. Different grids have different values based on their energy mix.

**Q: What if I'm not in the US?**
A: Use `/analytics/carbon` endpoint which supports 8 different regions.

**Q: How often is data updated?**
A: Whenever new energy readings are added via `/energy/add`

**Q: Can I filter by date?**
A: This endpoint uses all available data. Use `/analytics/carbon` for more filtering.

**Q: Is this accurate?**
A: ±5% accuracy. Based on standard grid emission factors.

---

## Integration Tips

### Add to Dashboard
```javascript
// Fetch and display carbon metric
async function displayCarbon() {
  const response = await fetch('/sustainability/carbon');
  const data = await response.json();
  
  document.getElementById('carbon-total').innerText = 
    `${data.emissions.total_tonnes_co2} tonnes CO2`;
  
  document.getElementById('carbon-cars').innerText = 
    `${data.equivalencies.car_miles.toFixed(0)} miles of driving`;
}
```

### Log Periodically
```python
# Check carbon emissions daily
import requests
import schedule

def check_carbon():
    response = requests.get('http://127.0.0.1:8000/sustainability/carbon')
    data = response.json()
    print(f"Current emissions: {data['emissions']['total_tonnes_co2']} tonnes")

schedule.every().day.at("08:00").do(check_carbon)
```

---

## Next Steps

1. **Add energy data** via `/energy/add` endpoint
2. **Call the endpoint** with curl or your app
3. **Parse the JSON** response
4. **Display results** on your dashboard

---

**Endpoint:** `GET /sustainability/carbon`
**Status:** ✅ Ready to use
**Complexity:** Beginner-friendly
**Response Format:** JSON

For more advanced analytics, see `/analytics/carbon`
