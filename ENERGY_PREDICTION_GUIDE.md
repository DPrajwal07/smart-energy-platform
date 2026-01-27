# Energy Consumption Prediction Model - Complete Guide

## Overview

This guide explains the **Linear Regression** model for predicting energy consumption. It's designed to be beginner-friendly and easy to understand.

## What is Linear Regression?

Linear Regression is the simplest machine learning algorithm. It works by:

1. **Learning a pattern**: Find the best straight line through historical data
2. **Making predictions**: Use that line to estimate future values

**Visual Example:**
```
Energy (kWh)
     ↑
  60 |     ○ (data point)
     |   ○   ○
  40 | ○_______→ Best-fit line
     | ○     ○
  20 | ○   ○
     |_______________→ Hour of Day
     0    6   12   18   24
```

## How the Model Works

### Step 1: Feature Engineering - Extract Time Patterns

Instead of just looking at raw timestamps, we extract useful features:

```python
# From a timestamp like "2026-01-27 14:30:00"
# We extract these features:

hour = 14              # Hour of day (0-23)
day_of_week = 2        # Day of week (0=Monday, 6=Sunday)
day_of_month = 27      # Day of month (1-31)
month = 1              # Month (1-12)
is_weekend = 0         # Is it weekend? (0 or 1)
is_business_hour = 1   # Is it 9am-5pm? (0 or 1)
```

**Why these features?**
- **Hour**: Energy use changes throughout the day (high at 2pm, low at 2am)
- **Day of week**: Weekday vs weekend patterns differ
- **Month**: Seasonal patterns (winter vs summer)
- **Is weekend**: Binary flag for quick pattern matching
- **Is business hour**: Peak usage detection

### Step 2: Train the Model

The model learns a **simple equation**:

```
Energy = Base + (Weight₁ × Hour) + (Weight₂ × DayOfWeek) + ...
```

**Example with real numbers:**

```
Energy = 22 + (1.5 × Hour) + (-2 × DayOfWeek) + (0.8 × Month) + ...
```

This means:
- Base consumption: 22 kWh
- Each hour increases energy by 1.5 kWh (during day) or decreases (at night)
- Weekends use 2 kWh less than weekdays
- Winter months use slightly more energy

### Step 3: Make Predictions

When you ask "How much energy on Friday at 2pm?"

```python
# Extract features
hour = 14
day_of_week = 4           # Friday
day_of_month = 27
month = 1
is_weekend = 0            # Friday is not weekend
is_business_hour = 1      # 2pm is business hours

# Calculate using the learned equation
Energy = 22 + (1.5 × 14) + (-2 × 4) + (0.8 × 1) + ...
Energy = 22 + 21 - 8 + 0.8 + ...
Energy ≈ 45.2 kWh
```

## Key Concepts Explained

### Features vs Target

| Concept | Definition | Example |
|---------|-----------|---------|
| **Features** | Input variables (X) | hour=14, day_of_week=4 |
| **Target** | What we predict (y) | 45.2 kWh |
| **Training** | Learning from examples | Show 1000 historical records |
| **Prediction** | Using learned pattern | Estimate future consumption |

### Model Accuracy Metrics

When training, the model reports three important metrics:

#### 1. R² Score (Coefficient of Determination)
- **Range**: 0 to 1
- **Meaning**: How well the model fits the data
- **Examples**:
  - **1.0** = Perfect predictions (rare)
  - **0.8** = Very good (explains 80% of variation)
  - **0.5** = Okay (explains 50% of variation)
  - **0.0** = No better than just guessing average

#### 2. MAE (Mean Absolute Error)
- **Unit**: kWh
- **Meaning**: Average prediction error
- **Example**: MAE = 3.2 kWh means average error is ±3.2 kWh

#### 3. RMSE (Root Mean Squared Error)
- **Unit**: kWh
- **Meaning**: Penalizes large errors more
- **Example**: RMSE = 4.1 kWh (emphasizes when predictions are way off)

## Advantages & Limitations

### ✅ Advantages
- **Simple**: Easy to understand and explain
- **Fast**: Trains quickly, makes predictions instantly
- **Interpretable**: You can see how each feature affects prediction
- **Reliable**: Works well for time-based patterns

### ⚠️ Limitations
- **Linear only**: Assumes straight-line relationship (not always true)
- **No memory**: Doesn't remember yesterday affects today
- **Weather ignored**: Doesn't account for temperature changes
- **Static patterns**: Assumes patterns don't change over time

## Using the Model in Code

### Basic Usage

```python
from energy_prediction_model import EnergyConsumptionPredictor
import pandas as pd
from datetime import datetime

# Step 1: Load historical data
data = pd.read_csv('energy_data.csv')
# Must have columns: 'timestamp' and 'energy_consumed_kwh'

# Step 2: Create and train the model
predictor = EnergyConsumptionPredictor()
metrics = predictor.train(data)

# Step 3: Make a single prediction
prediction = predictor.predict(datetime.now())
print(f"Predicted energy: {prediction['predicted_energy_kwh']} kWh")

# Step 4: Make multiple predictions (next 7 days, hourly)
forecast = predictor.predict_range(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=7),
    frequency='H'  # Hourly
)
print(forecast)
```

### Training Output Example

```
======================================================================
MODEL TRAINING COMPLETE
======================================================================
Coefficient of Determination (R² Score): 0.8342
  - 1.0 = Perfect predictions, 0.0 = No better than average
Mean Absolute Error (MAE): 2.31 kWh
  - Average difference from actual: ±2.31 kWh
Root Mean Squared Error (RMSE): 3.45 kWh
  - Penalizes large errors more heavily
======================================================================
Model Coefficients (weights for each feature):
  hour                    :   1.2341
  day_of_week             :  -0.5432
  day_of_month            :   0.0234
  month                   :   0.1234
  is_weekend              :  -1.5432
  is_business_hour        :   2.3421
Intercept (base energy):  22.5634 kWh
======================================================================
```

### Understanding the Coefficients

Each coefficient tells you the impact of one feature:

| Feature | Coefficient | Meaning |
|---------|------------|---------|
| hour | +1.23 | Each hour increase = +1.23 kWh |
| day_of_week | -0.54 | Each day later in week = -0.54 kWh |
| is_weekend | -1.54 | Weekend = 1.54 kWh less |
| is_business_hour | +2.34 | Business hours = +2.34 kWh |

## Example Walkthrough

### Scenario: Predict energy at Wednesday 2pm

**Step 1: Extract features**
```python
timestamp = datetime(2026, 1, 28, 14, 0)  # Wednesday 2pm

hour = 14                    # 2pm is hour 14
day_of_week = 2              # Wednesday is day 2
day_of_month = 28            # January 28th
month = 1                    # January
is_weekend = 0               # Not weekend
is_business_hour = 1         # 2pm is business hours
```

**Step 2: Apply the formula**
```
Energy = Base + (Features × Coefficients)
Energy = 22.56 + 
         (14 × 1.23) +       # Hour contribution
         (2 × -0.54) +       # Day of week contribution
         (28 × 0.023) +      # Day of month contribution
         (1 × 0.123) +       # Month contribution
         (0 × -1.54) +       # Weekend contribution
         (1 × 2.34)          # Business hour contribution

Energy = 22.56 + 17.22 - 1.08 + 0.64 + 0.123 + 0 + 2.34
Energy ≈ 41.88 kWh
```

**Step 3: Result**
```python
{
    'timestamp': '2026-01-28T14:00:00',
    'predicted_energy_kwh': 41.88,
    'features': {
        'hour': 14,
        'day_of_week': 2,
        'day_of_month': 28,
        'month': 1,
        'is_weekend': 0,
        'is_business_hour': 1
    }
}
```

## Data Requirements

To train the model effectively, you need:

### Minimum Data
- **100-200 records** for basic model
- **1000+ records** for reliable model
- **30+ days** of historical data (captures patterns)

### Data Format
```python
# CSV file with these columns:
timestamp,energy_consumed_kwh
2026-01-27 00:00:00,22.4
2026-01-27 01:00:00,18.2
2026-01-27 02:00:00,16.9
...
```

Or as Pandas DataFrame:
```python
df = pd.DataFrame({
    'timestamp': [...],
    'energy_consumed_kwh': [...]
})
```

## Improving Predictions

### Add More Features
The current model could be improved by adding:
- Temperature (major energy driver)
- Humidity (affects HVAC)
- Day type (holidays vs normal days)
- Special events (conferences increase usage)

### Use More Data
- **More records** = Better understanding of patterns
- **Longer history** = Captures seasonal patterns
- **Multiple years** = Accounts for yearly cycles

### Better Data Quality
- Remove outliers (sensor errors)
- Handle missing values (fill or remove)
- Ensure consistent timestamps

## When Linear Regression Works Well

✅ **Good for:**
- Time-based patterns (daily, weekly, seasonal)
- Stable, predictable consumption
- Quick, interpretable predictions
- When causation is clear (e.g., hour → consumption)

❌ **Not ideal for:**
- Sudden changes (broken equipment)
- Complex interactions (temperature + humidity together)
- Non-linear relationships (cost vs consumption)
- Rare events (storms, emergencies)

## Comparison with Other Models

| Model | Complexity | Accuracy | Speed | Interpretability |
|-------|-----------|----------|-------|-----------------|
| **Linear Regression** | Simple | Good | Very Fast | Excellent |
| Decision Tree | Medium | Very Good | Fast | Very Good |
| Neural Network | Complex | Excellent | Slow | Poor |
| Random Forest | Complex | Very Good | Medium | Medium |

## Common Questions

### Q: Why is the prediction sometimes negative?
**A:** The model has safeguards: `prediction = max(0, prediction)`. Negative values are set to 0 kWh (you can't use negative energy).

### Q: How often should I retrain the model?
**A:** 
- **Weekly**: If consumption patterns change slowly
- **Monthly**: Standard practice
- **Quarterly**: If patterns are stable
- **After changes**: New equipment, policy, etc.

### Q: Can I use this for multiple machines?
**A:** Yes! Either:
1. Train separate models per machine
2. Add machine_id as a feature to a single model

### Q: What if the R² is too low?
**A:** Try these:
- Add more training data
- Add new features (temperature, humidity)
- Check for outliers in data
- Use a more complex model

## Next Steps

1. **Run the demo**: `python energy_prediction_model.py`
2. **Integrate into your API**: Add FastAPI endpoint
3. **Monitor predictions**: Track real vs predicted
4. **Improve the model**: Collect more data
5. **Explore advanced models**: Neural networks, gradient boosting

## Files Provided

- **energy_prediction_model.py**: Complete model implementation (800+ lines)
  - `EnergyConsumptionPredictor` class
  - Time feature extraction
  - Training and prediction methods
  - Example usage and demo
  
- **ENERGY_PREDICTION_GUIDE.md**: This guide (comprehensive explanation)

## Technical Details

### Libraries Used
- **scikit-learn**: LinearRegression algorithm
- **pandas**: Data handling (DataFrames, date_range)
- **numpy**: Numerical computations
- **datetime**: Time manipulation

### Model Type
- **Algorithm**: Linear Regression (Ordinary Least Squares / OLS)
- **Complexity**: O(n × m) for training (n=records, m=features)
- **Memory**: O(m) for trained model (just stores coefficients)
- **Prediction Speed**: Sub-millisecond per prediction

### Mathematical Formula
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ

Where:
- y = predicted energy
- β₀ = intercept (base energy)
- βₙ = coefficients (weights)
- xₙ = features (hour, day_of_week, etc.)
```

## Troubleshooting

### Error: "Model must be trained before making predictions"
```python
# Solution: Train the model first
predictor.train(training_data)
predictor.predict(some_timestamp)  # Now this works
```

### Error: "Key error: 'timestamp' or 'energy_consumed_kwh'"
```python
# Solution: Ensure DataFrame has correct column names
df.columns  # Should be: ['timestamp', 'energy_consumed_kwh']
```

### Poor predictions (high error)
```python
# Solutions:
1. Use more training data (at least 1000 records)
2. Check data quality (outliers, missing values)
3. Ensure timestamp format is correct
4. Add more features (temperature, etc.)
5. Try a more complex model
```

---

**Status**: ✅ Production Ready
**Last Updated**: January 27, 2026
