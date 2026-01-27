# Carbon Footprint Calculation Guide

## Overview

The carbon footprint module calculates CO2 emissions from energy consumption data. It uses standard emission factors based on grid mix and provides comprehensive environmental impact analysis.

## Key Concepts

### 1. Emission Factor (kg CO2/kWh)

An emission factor represents how much CO2 is released per kilowatt-hour of electricity used.

**Why Different Values?**
- Different regions use different energy sources
- Coal-heavy grids have high emission factors
- Renewable-heavy grids have low emission factors

**Regional Emission Factors:**
```
France:            0.06 kg CO2/kWh  (mostly nuclear)
Renewable_Heavy:   0.10 kg CO2/kWh  (high renewable mix)
UK:                0.20 kg CO2/kWh  (natural gas + renewables)
US_Average:        0.385 kg CO2/kWh (DEFAULT - mixed sources)
Natural_Gas:       0.50 kg CO2/kWh  (natural gas dominant)
Germany:           0.38 kg CO2/kWh  (transitioning to renewables)
Coal_Heavy:        0.95 kg CO2/kWh  (mostly coal)
India:             0.92 kg CO2/kWh  (coal dependent)
```

### 2. Carbon Footprint Formula

**Basic Formula:**
```
CO2 Emissions (kg) = Energy Consumption (kWh) × Emission Factor (kg CO2/kWh)
```

**Example:**
```
Energy consumed: 1000 kWh
Emission factor: 0.385 kg CO2/kWh (US Average)
CO2 emitted:     1000 × 0.385 = 385 kg CO2 per day
```

### 3. Daily vs. Monthly

**Daily:** Sum of emissions for one day
**Monthly:** Sum of all daily emissions in a month

## Using the Carbon Footprint Module

### Option 1: Standalone Python Usage

```python
from carbon_footprint import (
    calculate_daily_co2_emissions,
    calculate_monthly_co2_from_dataframe,
    calculate_co2_with_breakdown
)
import pandas as pd

# Single day calculation
daily_co2 = calculate_daily_co2_emissions(500)  # 500 kWh
print(f"Daily CO2: {daily_co2:.2f} kg")  # Output: 192.50 kg

# Monthly calculation from DataFrame
df = pd.DataFrame({
    'timestamp': pd.date_range('2026-01-01', periods=48, freq='30min'),
    'energy_consumed_kwh': [50, 55, 48, ...] * 6
})

daily_breakdown, monthly_total = calculate_monthly_co2_from_dataframe(df)
print(f"Monthly Total: {monthly_total:.2f} kg CO2")

# Comprehensive report
report = calculate_co2_with_breakdown(df, region='US_Average')
print(report['summary'])
print(report['equivalencies'])
```

### Option 2: REST API Endpoint

**GET `/analytics/carbon`**

Calculates carbon footprint directly from database energy readings.

#### Parameters:

```
machine_id (optional)     Filter to specific machine
region (optional)         Grid region for emission factor
                         Default: "US_Average"
```

#### Example Requests:

**All machines, US average:**
```bash
curl http://127.0.0.1:8000/analytics/carbon
```

**Specific machine, different region:**
```bash
curl "http://127.0.0.1:8000/analytics/carbon?machine_id=PUMP-01&region=Renewable_Heavy"
```

#### Example Response:

```json
{
  "analysis_date": "2026-01-26T14:30:45.123456",
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
    },
    {
      "date": "2026-01-02",
      "total_energy_kwh": 480,
      "co2_kg": 184.8
    }
  ],
  
  "equivalencies": {
    "car_miles_equivalent": 11726.34,
    "trees_needed_per_year": 289.35,
    "car_months_equivalent": 12.52,
    "description": {
      "car_miles_equivalent": "Equivalent miles of car driving",
      "trees_needed_per_year": "Trees needed to offset yearly emissions",
      "car_months_equivalent": "Months of average car emissions"
    }
  },
  
  "insights": {
    "observations": [
      "High monthly emissions: 4.8 tonnes CO2"
    ],
    "recommendations": [
      "Consider energy efficiency improvements",
      "Explore renewable energy options",
      "Implement demand management"
    ]
  }
}
```

## Understanding the Results

### Summary Statistics

- **total_energy_kwh:** Total energy consumed in analyzed period
- **monthly_co2_kg:** Total CO2 emissions in kilograms
- **monthly_co2_tonnes:** Same in metric tonnes (1 tonne = 1000 kg)
- **daily_average_co2_kg:** Mean daily emissions
- **daily_min_co2_kg:** Lowest single-day emissions
- **daily_max_co2_kg:** Highest single-day emissions

### Daily Breakdown

Shows CO2 for each day, helps identify:
- Peak consumption days
- Trends over time
- Anomalies or unusual patterns

### Equivalencies

Real-world comparisons to make impact clear:

**Example (Monthly emissions = 4812.5 kg):**
- **Car miles: 11,726 miles** - Equivalent driving distance (~0.41 kg CO2/km)
- **Trees needed: 289** - Number of trees needed to absorb yearly emissions at this rate
- **Car months: 12.5 months** - Equivalent to average car usage for this duration

### Insights

**Observations:**
- Categorizes emissions (Low/Moderate/High)
- Shows daily average consumption

**Recommendations:**
- Suggests actions based on consumption level
- Targets for efficiency improvements
- Monitoring best practices

## Example Calculations

### Scenario 1: Office Building (US Average Grid)

```
Daily energy use:    1000 kWh
Emission factor:     0.385 kg CO2/kWh
Daily CO2:           1000 × 0.385 = 385 kg CO2
Monthly CO2:         385 × 30 = 11,550 kg = 11.55 tonnes

Equivalencies:
- Driving: 28,171 miles of car use
- Trees: 693 trees/year to offset
- Car: 30 months of driving
```

### Scenario 2: Manufacturing Plant (Coal-Heavy Region)

```
Daily energy use:    5000 kWh
Emission factor:     0.95 kg CO2/kWh
Daily CO2:           5000 × 0.95 = 4,750 kg CO2
Monthly CO2:         4,750 × 30 = 142,500 kg = 142.5 tonnes

Impact:
- High monthly emissions
- Need significant efficiency measures
- Renewable energy investment recommended
```

### Scenario 3: Data Center (Renewable-Heavy Region)

```
Daily energy use:    8000 kWh
Emission factor:     0.10 kg CO2/kWh (clean grid)
Daily CO2:           8000 × 0.10 = 800 kg CO2
Monthly CO2:         800 × 30 = 24,000 kg = 24 tonnes

Benefit:
- Low carbon per kWh despite high usage
- Location choice matters for sustainability
```

## Integration with Energy Data

### Data Requirements

Your energy data DataFrame should have:
- **timestamp:** When energy was consumed
- **energy_consumed_kwh:** Energy in kilowatt-hours

### Example DataFrame:

```python
import pandas as pd
from datetime import datetime, timedelta

# Create sample data
start = datetime(2026, 1, 1)
df = pd.DataFrame({
    'timestamp': [start + timedelta(hours=i) for i in range(24)],
    'machine_id': ['PUMP-01'] * 24,
    'power_kw': [50, 48, 52, 55, ...],
    'energy_consumed_kwh': [50, 48, 52, 55, ...]
})

# Calculate carbon
from carbon_footprint import calculate_co2_with_breakdown
report = calculate_co2_with_breakdown(df)
```

## Comparing Regions

Use `compare_emission_factors()` to see how emissions differ by region:

```python
from carbon_footprint import compare_emission_factors

# For 1000 kWh of energy
comparison = compare_emission_factors(1000)

for region, data in sorted(comparison.items(), key=lambda x: x[1]['co2_kg']):
    print(f"{region:20} {data['co2_kg']:6.1f} kg CO2")

# Output:
# France                 60.0 kg CO2
# Renewable_Heavy       100.0 kg CO2
# UK                    200.0 kg CO2
# US_Average            385.0 kg CO2
# Natural_Gas           500.0 kg CO2
# Coal_Heavy            950.0 kg CO2
```

## Best Practices

### 1. Choose Accurate Emission Factor
- Know your grid mix (check regional electricity provider)
- Update if grid changes (more renewables added)
- Use specific region if possible, not US average

### 2. Aggregate at Right Level
- Daily aggregation catches trends
- Weekly/monthly for overall trends
- Hourly for detailed anomaly detection

### 3. Use Equivalencies Wisely
- Help communicate impact to stakeholders
- Show progress on sustainability goals
- Set reduction targets

### 4. Monitor Trends
- Track monthly emissions over time
- Identify efficiency improvements
- Validate impact of energy changes

### 5. Act on Insights
- High usage → implement efficiency measures
- Renewable regions → cheaper green energy
- Peak patterns → demand management

## Environmental Context

### Why Carbon Matters?

1 kg CO2 = emissions from:
- Burning 0.41 liters of gasoline
- Driving 3.2 km in a car
- Running a 60W light for 20 hours

### Carbon Reduction Goals

Typical targets:
- 5% annual reduction (continuous improvement)
- 25% reduction (major efficiency push)
- 50% reduction (renewable transition)
- 100% reduction (net-zero goal)

### Offsetting

To offset 1 tonne CO2:
- Plant ~40-50 trees
- Or fund renewable energy projects
- Or purchase verified carbon credits

## Troubleshooting

### Issue: Unexpected High Emissions
**Check:**
- Is emission factor correct for your region?
- Is energy data in kWh (not MWh)?
- Are there anomalies in the data?

### Issue: Region Not Available
**Solution:**
```python
# Use nearest region, or specify custom factor
from carbon_footprint import calculate_co2_with_breakdown

report = calculate_co2_with_breakdown(
    df,
    emission_factor=0.4  # Custom value
)
```

### Issue: No Data
**Ensure:**
- DataFrame has 'timestamp' and 'energy_consumed_kwh' columns
- Data is recent enough (not too old)
- Query filters (machine_id) match actual data

## Further Reading

- **EPA Emission Factors:** https://www.epa.gov/energy
- **Carbon Trust:** https://www.carbontrust.com/
- **IEA Grid Mix Data:** https://www.iea.org/
- **Net Zero Goals:** https://www.un.org/en/climatechange/net-zero-coalition

---

**Last Updated:** January 2026
**Module Version:** 1.0
**Status:** Production Ready
