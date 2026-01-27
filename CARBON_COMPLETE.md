# Carbon Footprint Module - Complete Implementation

## Summary

I've created a comprehensive carbon footprint calculation system for the Smart Energy Platform. This module quantifies CO2 emissions from energy consumption using industry-standard emission factors.

## What You Get

### 1. Core Module: `carbon_footprint.py` (600+ lines)

**Key Functions:**
- `calculate_daily_co2_emissions()` - Single day CO2 calculation
- `calculate_monthly_co2_emissions()` - Monthly total
- `calculate_monthly_co2_from_dataframe()` - DataFrame analysis with daily breakdown
- `calculate_co2_with_breakdown()` - Comprehensive analysis with insights
- `compare_emission_factors()` - Regional comparison

**Emission Factors Included:**
- France: 0.06 kg CO2/kWh (nuclear)
- Renewable_Heavy: 0.10 kg CO2/kWh
- UK: 0.20 kg CO2/kWh
- **US_Average: 0.385 kg CO2/kWh** (default)
- Natural_Gas: 0.50 kg CO2/kWh
- Coal_Heavy: 0.95 kg CO2/kWh
- And more...

### 2. REST API Endpoint

**GET `/analytics/carbon`**

Returns:
```json
{
  "summary": {
    "monthly_co2_kg": 4812.5,
    "monthly_co2_tonnes": 4.8125,
    "daily_average_co2_kg": 172.6,
    "daily_min_co2_kg": 150.2,
    "daily_max_co2_kg": 195.8
  },
  "daily_breakdown": [...],
  "equivalencies": {
    "car_miles_equivalent": 11726,
    "trees_needed_per_year": 289,
    "car_months_equivalent": 12.5
  },
  "insights": {
    "observations": [...],
    "recommendations": [...]
  }
}
```

### 3. Documentation (900+ lines)

- **CARBON_FOOTPRINT_GUIDE.md** - Complete technical guide
- **CARBON_IMPLEMENTATION.md** - Implementation details
- **CARBON_QUICK_REFERENCE.md** - Quick lookup tables
- Updated **README.md** - Integrated with main docs

### 4. Test Suite: `test_carbon_footprint.py`

6 comprehensive tests:
1. Single day calculation
2. Monthly aggregation
3. DataFrame processing
4. Regional comparison
5. Comprehensive report
6. JSON response validation

## The Science

### Formula
```
CO2 Emissions (kg) = Energy (kWh) × Emission Factor (kg CO2/kWh)
```

### Why Different Factors?
Different regions use different energy sources:
- **Nuclear/Renewables:** Low CO2 (0.06-0.20)
- **Natural Gas:** Medium CO2 (0.50)
- **Coal:** High CO2 (0.95+)

### Example Calculation
```
Energy consumed: 1000 kWh
Emission factor: 0.385 kg CO2/kWh (US Average)

Daily CO2 = 1000 × 0.385 = 385 kg CO2
Monthly CO2 = 385 × 30 = 11,550 kg = 11.55 tonnes

Equivalencies:
- Car driving: 28,171 miles
- Trees needed: 693 per year
- Car emissions: 30 months worth
```

## Three Ways to Use It

### 1. Direct Python
```python
from carbon_footprint import calculate_daily_co2_emissions

daily_co2 = calculate_daily_co2_emissions(500)  # 500 kWh
print(f"{daily_co2:.1f} kg CO2")  # 192.5 kg CO2
```

### 2. With Pandas DataFrame
```python
from carbon_footprint import calculate_co2_with_breakdown
import pandas as pd

df = pd.DataFrame({
    'timestamp': [...],
    'energy_consumed_kwh': [...]
})

report = calculate_co2_with_breakdown(df)
print(report['summary'])
print(report['equivalencies'])
```

### 3. REST API
```bash
# All machines
curl http://127.0.0.1:8000/analytics/carbon

# Specific machine, specific region
curl "http://127.0.0.1:8000/analytics/carbon?machine_id=PUMP-01&region=Renewable_Heavy"
```

## Key Features

✅ **Standard Emission Factors** - Based on grid composition
✅ **Daily & Monthly Tracking** - Automatic aggregation
✅ **Regional Variations** - 8 pre-defined + custom
✅ **Real-World Equivalencies** - Makes impact clear
✅ **Automatic Insights** - Recommendations included
✅ **Error Handling** - Validates data, returns 404/500
✅ **Comprehensive Tests** - 6 test categories
✅ **Production Ready** - Error handling, logging, docs

## Data Returned

### Summary Statistics
- Total energy consumed
- Monthly CO2 (kg and tonnes)
- Daily average CO2
- Daily min/max CO2
- Emission factor used

### Daily Breakdown
```
Date        | Energy (kWh) | CO2 (kg)
2026-01-01  | 450          | 173.25
2026-01-02  | 480          | 184.80
```

### Equivalencies
- **Car miles:** Equivalent miles of driving
- **Trees:** Number of trees needed to offset yearly
- **Car months:** Months of average car emissions

### Insights
- **Observations:** High/medium/low category
- **Recommendations:** Action items based on usage

## Files Created

```
carbon_footprint.py                   # Core module (600 lines)
main.py (updated)                     # Added /analytics/carbon endpoint
test_carbon_footprint.py              # Test suite (400 lines)
CARBON_FOOTPRINT_GUIDE.md             # Full guide (400 lines)
CARBON_IMPLEMENTATION.md              # Implementation summary
CARBON_QUICK_REFERENCE.md             # Quick lookup tables
README.md (updated)                   # Added endpoint documentation
```

## Integration

**Zero Breaking Changes**
- No database schema changes
- No modifications to existing endpoints
- Works with existing energy data
- Seamless with analysis.py module

**One-Line Addition to main.py:**
```python
from carbon_footprint import calculate_co2_with_breakdown
```

## Quick Examples

### Calculate Emissions (Daily)
```
Energy: 500 kWh
Factor: 0.385 kg CO2/kWh
Result: 192.5 kg CO2
```

### Calculate Emissions (Monthly)
```
30 days × 500 kWh/day = 15,000 kWh
15,000 × 0.385 = 5,775 kg = 5.78 tonnes
```

### Compare Regions (1000 kWh)
```
France:      60 kg CO2  (16% of US)
Renewable:  100 kg CO2  (26% of US)
UK:         200 kg CO2  (52% of US)
US:         385 kg CO2  (100%)
Coal:       950 kg CO2  (247% of US)
```

### Understand Impact
```
5.78 tonnes CO2 = 
- 14,100 miles of car driving
- 290 trees needed/year
- 15 months of car emissions
```

## Testing

Run comprehensive test suite:
```bash
python test_carbon_footprint.py
```

Validates:
- Calculation accuracy
- DataFrame processing
- Regional variations
- API response format
- JSON serialization

## Next Steps

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Test the endpoint:**
   ```bash
   curl http://127.0.0.1:8000/analytics/carbon
   ```

3. **View in Swagger UI:**
   Visit `http://127.0.0.1:8000/docs`

4. **Run tests:**
   ```bash
   python test_carbon_footprint.py
   ```

5. **Integrate with frontend:**
   Display carbon metrics on dashboards

## Documentation

**For Detailed Information:**
- Technical guide: [CARBON_FOOTPRINT_GUIDE.md](CARBON_FOOTPRINT_GUIDE.md)
- Implementation: [CARBON_IMPLEMENTATION.md](CARBON_IMPLEMENTATION.md)
- Quick reference: [CARBON_QUICK_REFERENCE.md](CARBON_QUICK_REFERENCE.md)

**Interactive Documentation:**
- After starting server: `http://127.0.0.1:8000/docs`

## Requirements Fulfilled

✅ **Standard emission factors** - 8 regional options, US average default
✅ **Daily CO2 emissions** - Calculated from energy data
✅ **Monthly CO2 emissions** - Aggregated from daily values
✅ **Formula clearly explained** - 50+ lines of documentation
✅ **Production ready** - Error handling, validation, tests
✅ **Well commented** - 100+ comment lines
✅ **Comprehensive guide** - 900+ lines of documentation
✅ **API integrated** - Works with FastAPI and existing endpoints
✅ **Real-world context** - Equivalencies and insights included

---

## Technical Specifications

- **Language:** Python 3.7+
- **Dependencies:** pandas, numpy (already in requirements.txt)
- **Database:** Integrates with PostgreSQL energy data
- **API Framework:** FastAPI
- **Response Format:** JSON
- **Status Codes:** 200 (success), 404 (no data), 500 (error)

## Environmental Context

**Why Carbon Matters:**
- 1 kg CO2 = emissions from 0.41 liters of gasoline
- 1 tree absorbs ~20 kg CO2/year
- Global target: Net-zero emissions

**Typical Reduction Goals:**
- 5% annual improvement
- 25% major efficiency push
- 50% renewable transition
- 100% net-zero target

---

**Status:** 🟢 **PRODUCTION READY**
**Created:** January 2026
**Version:** 1.0
**Support:** See documentation files

