# Carbon Footprint Quick Reference

## Formula at a Glance

```
CO2 (kg) = Energy (kWh) × Emission Factor (kg CO2/kWh)
```

## Regional Emission Factors

| Region | Factor | Grid Mix |
|--------|--------|----------|
| France | 0.06 | Nuclear (75%) |
| Renewable_Heavy | 0.10 | Renewables (80%+) |
| UK | 0.20 | Gas + Renewables |
| **US_Average** | **0.385** | **Mixed (default)** |
| Germany | 0.38 | Transitioning |
| Natural_Gas | 0.50 | Natural Gas |
| Coal_Heavy | 0.95 | Coal Dominant |
| India | 0.92 | Coal Heavy |

## Common Conversions

```
1 kg CO2  = 0.41 liters of gasoline
1 kg CO2  = 3.2 km of car driving
1 tonne   = 1000 kg CO2
1 tree    = ~20 kg CO2 absorbed/year
```

## Examples (US Average: 0.385 kg CO2/kWh)

### Small Office
```
Daily: 500 kWh × 0.385 = 192.5 kg CO2 = 0.19 tonnes
Monthly: 192.5 × 30 = 5,775 kg = 5.78 tonnes
Impact: ≈ 14,100 miles of driving
Trees: ≈ 35 trees/year to offset
```

### Manufacturing Plant
```
Daily: 5000 kWh × 0.385 = 1,925 kg CO2 = 1.93 tonnes
Monthly: 1,925 × 30 = 57,750 kg = 57.75 tonnes
Impact: ≈ 141,000 miles of driving
Trees: ≈ 347 trees/year to offset
```

### Data Center
```
Daily: 8000 kWh × 0.385 = 3,080 kg CO2 = 3.08 tonnes
Monthly: 3,080 × 30 = 92,400 kg = 92.4 tonnes
Impact: ≈ 225,000 miles of driving
Trees: ≈ 555 trees/year to offset
```

## Python Quick Usage

### Single Day
```python
from carbon_footprint import calculate_daily_co2_emissions

co2 = calculate_daily_co2_emissions(1000)  # 1000 kWh
print(f"{co2:.1f} kg CO2")  # 385.0 kg CO2
```

### Monthly from DataFrame
```python
from carbon_footprint import calculate_monthly_co2_from_dataframe
import pandas as pd

df = pd.DataFrame({
    'timestamp': [...],
    'energy_consumed_kwh': [...]
})

daily, monthly = calculate_monthly_co2_from_dataframe(df)
print(f"Monthly: {monthly:.1f} kg CO2")
```

### Full Analysis
```python
from carbon_footprint import calculate_co2_with_breakdown

report = calculate_co2_with_breakdown(df, region='US_Average')
print(report['summary'])  # Complete stats
print(report['equivalencies'])  # Car miles, trees, etc.
```

## API Quick Usage

### cURL Examples

**All machines:**
```bash
curl http://127.0.0.1:8000/analytics/carbon
```

**Specific machine:**
```bash
curl "http://127.0.0.1:8000/analytics/carbon?machine_id=PUMP-01"
```

**Different region:**
```bash
curl "http://127.0.0.1:8000/analytics/carbon?region=Renewable_Heavy"
```

### Python Requests

```python
import requests

# All machines
r = requests.get('http://127.0.0.1:8000/analytics/carbon')
data = r.json()

# Specific machine
r = requests.get(
    'http://127.0.0.1:8000/analytics/carbon',
    params={'machine_id': 'PUMP-01'}
)
```

## Understanding Results

### Summary Stats
```python
summary = {
    'monthly_co2_kg': 4812.5,        # Total monthly CO2
    'monthly_co2_tonnes': 4.8125,    # Same in tonnes
    'daily_average_co2_kg': 172.6,   # Mean per day
    'daily_min_co2_kg': 150.2,       # Lowest day
    'daily_max_co2_kg': 195.8        # Highest day
}
```

### Daily Breakdown
```python
daily = [
    {'date': '2026-01-01', 'total_energy_kwh': 450, 'co2_kg': 173.25},
    {'date': '2026-01-02', 'total_energy_kwh': 480, 'co2_kg': 184.80}
]
```

### Equivalencies
```python
equiv = {
    'car_miles_equivalent': 11726,      # Miles of driving
    'trees_needed_per_year': 289,       # Trees to offset
    'car_months_equivalent': 12.5       # Months of car usage
}
```

## Regional Impact (1000 kWh)

```
France:             60 kg CO2  (16% of US)
Renewable:         100 kg CO2  (26% of US)
UK:                200 kg CO2  (52% of US)
US Average:        385 kg CO2  (100%)
Germany:           380 kg CO2  (99% of US)
Natural Gas:       500 kg CO2  (130% of US)
Coal Heavy:        950 kg CO2  (247% of US)
```

**Key Insight:** Location matters! Moving to a cleaner grid reduces emissions by 75%+.

## Reduction Targets

### 5% Reduction (Annual)
```
Current: 100 tonnes CO2/month
Target:  95 tonnes CO2/month
Action:  Incremental efficiency improvements
Timeline: Ongoing
```

### 25% Reduction
```
Current: 100 tonnes CO2/month
Target:  75 tonnes CO2/month
Action:  Major efficiency push + some renewables
Timeline: 2-3 years
```

### 50% Reduction
```
Current: 100 tonnes CO2/month
Target:  50 tonnes CO2/month
Action:  Renewable transition + efficiency
Timeline: 3-5 years
```

## Sustainability Actions

### Low Cost
- [ ] LED lighting upgrades
- [ ] HVAC optimization
- [ ] Demand management
- [ ] Equipment maintenance
- [ ] Peak shaving strategies

### Medium Cost
- [ ] Solar panels (5-10 kW)
- [ ] Energy management system
- [ ] Equipment replacement
- [ ] Building insulation
- [ ] Renewable energy contracts

### High Impact
- [ ] Major renewable installation (50+ kW)
- [ ] Grid operator switch (cleaner provider)
- [ ] Carbon offset programs
- [ ] Facilities redesign
- [ ] Process optimization

## Carbon Offset Options

### Trees
```
1 tree = ~20 kg CO2/year
For 100 tonnes/month = 60,000 kg/year
Need: 3,000 trees
Area: ~30 acres
Cost: $30,000-$150,000/year
```

### Renewable Energy
```
Cost: $50-$200/tonne CO2 avoided
1 MW solar = ~1,500 tonnes/year saved
ROI: 5-10 years
```

### Carbon Credits
```
Cost: $10-$30/tonne CO2
Verified programs
Third-party certified
Tradeable markets
```

## Testing Module

Run tests to verify calculations:
```bash
python test_carbon_footprint.py
```

Tests include:
- Single day calculations
- Monthly aggregations
- DataFrame processing
- Regional comparisons
- Comprehensive reports
- API response validation

## Common Questions

**Q: Why does my carbon differ by region?**
A: Different regions use different energy sources. Coal produces more CO2 than renewables.

**Q: How accurate are these calculations?**
A: Typical ±5% accuracy. Based on average grid composition, not real-time mix.

**Q: Can I use a custom emission factor?**
A: Yes, pass `emission_factor=0.5` to any function.

**Q: What's the best region to move to?**
A: France (0.06), Renewable-heavy areas (0.10), UK (0.20).

**Q: How do I offset carbon?**
A: Plant trees, buy renewable energy, purchase verified carbon credits.

## Documentation

- Full guide: [CARBON_FOOTPRINT_GUIDE.md](CARBON_FOOTPRINT_GUIDE.md)
- Implementation: [CARBON_IMPLEMENTATION.md](CARBON_IMPLEMENTATION.md)
- API Docs: Visit `http://127.0.0.1:8000/docs` after starting server

---

**Last Updated:** January 2026
**Status:** Production Ready
