# Energy Data Analysis Guide

This guide explains how to use the energy analysis module with your Smart Energy Platform API.

## Overview

The `analysis.py` module provides four main functions for analyzing energy consumption data using Pandas:

1. **Calculate Daily Consumption** - Sum up energy usage by day
2. **Identify Peak Periods** - Find high-load time periods
3. **Detect Abnormal Spikes** - Find unusual consumption patterns
4. **Generate Report** - Comprehensive analysis summary

---

## 1. Daily Energy Consumption Analysis

### Purpose
Calculate total energy consumed each day from hourly/minute readings.

### Function
```python
from analysis import calculate_daily_consumption

daily = calculate_daily_consumption(df, energy_column='energy_consumed_kwh')
```

### How It Works
1. Group readings by date (removes time component)
2. Sum energy for each day
3. Return DataFrame with date and total_energy_kwh

### Example Output
```
        date  total_energy_kwh
0  2026-01-01          1250.75
1  2026-01-02          1340.20
2  2026-01-03          1180.50
```

### Use Cases
- Daily energy billing
- Trend analysis (which days use most energy?)
- Identify changes in consumption patterns
- Monthly/weekly comparisons

---

## 2. Peak Load Period Identification

### Purpose
Identify periods of high power consumption using percentile analysis.

### Function
```python
from analysis import identify_peak_periods

peaks = identify_peak_periods(df, power_column='power_kw', percentile=75)
```

### How It Works
1. Calculate 75th percentile of power (configurable)
2. Count readings above this threshold
3. Calculate peak load statistics

### Example Output
```python
{
    'peak_threshold': 52.03,        # Power level considered "peak"
    'peak_count': 12,               # 12 readings were at peak
    'peak_percentage': 25.0,        # 25% of time is peak load
    'average_peak_power': 70.01,    # Average during peaks
    'min_peak_power': 52.48,
    'max_peak_power': 150.0
}
```

### Parameters
- `percentile`: 50 = median, 75 = upper quartile, 90 = very high loads
- Lower percentile = more "peak" periods
- Higher percentile = only extreme peaks

### Use Cases
- Capacity planning (size generators/infrastructure)
- Demand response programs (reduce usage during peaks)
- Time-of-use billing
- Identify when machines are running hard

---

## 3. Abnormal Spike Detection (Rolling Average)

### Purpose
Detect unusual power consumption spikes using statistical methods.

### Function
```python
from analysis import detect_abnormal_spikes

anomalies = detect_abnormal_spikes(
    df,
    power_column='power_kw',
    window_size=5,              # Rolling window: 5 readings
    deviation_threshold=2.0     # 2 std deviations
)
```

### How It Works

**Rolling Average:**
```
Normal readings: [10, 12, 11, 13, 12, 50, 12, 11, 10]
Rolling avg(3): [-, -, 11, 12, 12, 25, 25, 24, 11]
```

**Deviation Calculation:**
```
Deviation = Actual - Rolling Average
           = 50 - 25 = +25
```

**Anomaly Detection:**
- Calculate standard deviation of all deviations
- If deviation > 2 × std_dev, flag as anomaly
- 2.0 threshold = ~95% confidence (statistically normal)

### Example Output
```python
DataFrame with columns:
- power_kw: Original power value
- rolling_avg: Smoothed average
- deviation: Difference from average
- is_anomaly: True/False flag

Anomalies Found:
            timestamp  power_kw  rolling_avg  deviation  is_anomaly
20 2026-01-01 10:00:00    150.0       66.98       83.02        True
35 2026-01-01 17:30:00    140.0       69.60       70.40        True
```

### Parameters
- `window_size`: Larger = smoother trend (default: 5)
  - Small (3): Detects quick changes
  - Large (10): Detects only big deviations
- `deviation_threshold`: How strict (default: 2.0)
  - 1.0: More sensitive (more false positives)
  - 2.0: Balanced
  - 3.0: Very strict (only extreme outliers)

### Use Cases
- Equipment malfunction detection
- Energy theft detection
- Quality assurance (verify readings)
- Maintenance alerts (something isn't working right)

---

## 4. Comprehensive Analysis Report

### Purpose
Generate a complete analysis summary in one call.

### Function
```python
from analysis import generate_analysis_report

report = generate_analysis_report(
    df,
    machine_id='MACHINE-001',
    power_column='power_kw',
    energy_column='energy_consumed_kwh'
)
```

### Example Output
```python
{
    'machine_id': 'MACHINE-001',
    'analysis_date': '2026-01-26T10:30:00.123456',
    'data_points': 48,
    
    'daily_consumption': {
        'total_days': 1,
        'average_daily_kwh': 1269.75,
        'min_daily_kwh': 1269.75,
        'max_daily_kwh': 1269.75,
        'daily_data': [...]
    },
    
    'peak_load': {
        'peak_threshold': 52.03,
        'peak_count': 12,
        'peak_percentage': 25.0,
        'average_peak_power': 70.01,
        ...
    },
    
    'anomalies': {
        'anomaly_count': 2,
        'anomaly_percentage': 4.17,
        'anomalous_readings': [
            {'power_kw': 150.0, 'rolling_avg': 66.98, 'deviation': 83.02},
            {'power_kw': 140.0, 'rolling_avg': 69.60, 'deviation': 70.40}
        ]
    },
    
    'overall_statistics': {
        'average_power_kw': 52.91,
        'min_power_kw': 47.65,
        'max_power_kw': 150.0,
        'std_deviation_kw': 18.45,
        'total_energy_kwh': 1269.75
    }
}
```

---

## Integration with FastAPI

### Example 1: Analyze Data from Database

```python
from fastapi import FastAPI
from sqlalchemy.orm import Session
import pandas as pd
from analysis import generate_analysis_report

@app.get("/analyze/{machine_id}")
def analyze_machine(machine_id: str, db: Session = Depends(get_db)):
    # Query readings from database
    readings = db.query(EnergyReading).filter(
        EnergyReading.machine_id == machine_id
    ).all()
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'timestamp': r.timestamp,
            'power_kw': r.power_kw,
            'energy_consumed_kwh': r.energy_consumed_kwh,
            'machine_id': r.machine_id
        }
        for r in readings
    ])
    
    # Generate report
    report = generate_analysis_report(df, machine_id=machine_id)
    
    return report
```

### Example 2: Daily Summary

```python
@app.get("/daily-summary/{machine_id}")
def daily_summary(machine_id: str, db: Session = Depends(get_db)):
    readings = db.query(EnergyReading).filter(
        EnergyReading.machine_id == machine_id
    ).all()
    
    df = pd.DataFrame([
        {'timestamp': r.timestamp, 'energy_consumed_kwh': r.energy_consumed_kwh}
        for r in readings
    ])
    
    daily = calculate_daily_consumption(df)
    return daily.to_dict('records')
```

### Example 3: Alert on Anomalies

```python
@app.get("/anomalies/{machine_id}")
def get_anomalies(machine_id: str, db: Session = Depends(get_db)):
    readings = db.query(EnergyReading).filter(
        EnergyReading.machine_id == machine_id
    ).all()
    
    df = pd.DataFrame([
        {'power_kw': r.power_kw, 'timestamp': r.timestamp}
        for r in readings
    ])
    
    anomalies = detect_abnormal_spikes(df)
    
    # Return only anomalies
    anomalies_found = anomalies[anomalies['is_anomaly']]
    
    return {
        'anomaly_count': len(anomalies_found),
        'anomalies': anomalies_found.to_dict('records')
    }
```

---

## Common Analysis Patterns

### Pattern 1: Energy Bill Calculation
```python
daily = calculate_daily_consumption(df)
daily['cost_usd'] = daily['total_energy_kwh'] * 0.12  # $0.12 per kWh
monthly_cost = daily['cost_usd'].sum()
```

### Pattern 2: Peak Demand Charge
```python
peaks = identify_peak_periods(df, percentile=90)
peak_power_charge = peaks['max_peak_power'] * 15  # $15 per kW
```

### Pattern 3: Equipment Health Check
```python
anomalies = detect_abnormal_spikes(df, window_size=10, deviation_threshold=3)
if anomalies['is_anomaly'].any():
    alert_maintenance("Equipment running abnormally")
```

### Pattern 4: Compare Machines
```python
for machine_id in ['MACHINE-001', 'MACHINE-002', 'MACHINE-003']:
    df = get_machine_data(machine_id)
    report = generate_analysis_report(df, machine_id)
    print(f"{machine_id}: {report['overall_statistics']['average_power_kw']} kW avg")
```

---

## Performance Tips

### For Large Datasets
```python
# Load only recent data
from datetime import datetime, timedelta
since = datetime.now() - timedelta(days=30)

readings = db.query(EnergyReading).filter(
    EnergyReading.timestamp >= since
).all()
```

### Optimize Pandas Operations
```python
# Use efficient data types
df['power_kw'] = df['power_kw'].astype('float32')  # Instead of float64
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter before grouping
df_filtered = df[df['power_kw'] > 0]
daily = calculate_daily_consumption(df_filtered)
```

---

## Troubleshooting

### Issue: No anomalies detected
**Solution:** Adjust `deviation_threshold` lower (e.g., 1.5 instead of 2.0)

### Issue: Too many false anomalies
**Solution:** Increase `window_size` (smooth out normal fluctuations) or raise `deviation_threshold`

### Issue: Peak percentage is 50%
**Solution:** Use higher percentile (e.g., 90 instead of 75)

---

## Further Reading

- **Rolling Average**: Smoothing technique for time-series data
- **Standard Deviation**: Measure of variation (2.0σ ≈ 95% confidence)
- **Percentiles**: Divide data into 100 equal parts
- **Time-Series Analysis**: Analyzing data collected over time

---

Created for Smart Energy Platform | January 2026
