# Energy Prediction Model - Code Examples & Usage Patterns

## 🎯 Quick Copy-Paste Examples

### Example 1: Basic Usage (Standalone)

```python
from energy_prediction_model import EnergyConsumptionPredictor
import pandas as pd
from datetime import datetime

# Load your energy data
df = pd.read_csv('energy_data.csv')
# Must have columns: 'timestamp', 'energy_consumed_kwh'

# Create and train model
predictor = EnergyConsumptionPredictor()
metrics = predictor.train(df)

# Predict for tomorrow at 2pm
tomorrow_2pm = datetime(2026, 1, 28, 14, 0)
prediction = predictor.predict(tomorrow_2pm)

print(f"Predicted energy: {prediction['predicted_energy_kwh']} kWh")
# Output: Predicted energy: 45.23 kWh
```

### Example 2: Multiple Predictions

```python
from datetime import datetime, timedelta

# Predict for next 7 days (hourly)
start = datetime.now()
end = start + timedelta(days=7)

forecast = predictor.predict_range(start, end, frequency='H')
print(forecast.head(10))
# Returns DataFrame with 168 hourly predictions
```

### Example 3: Get Model Explanation

```python
explanation = predictor.explain_model()
print(explanation)

# Shows:
# - Formula used
# - How each feature affects energy
# - Example calculation
```

### Example 4: Check Model Accuracy

```python
metrics = predictor.train(df)

print(f"R² Score: {metrics['r2_score']:.4f}")
print(f"MAE: {metrics['mae']:.2f} kWh")
print(f"RMSE: {metrics['rmse']:.2f} kWh")
print(f"Coefficients: {metrics['coefficients']}")

# Output example:
# R² Score: 0.8342
# MAE: 2.31 kWh
# RMSE: 3.45 kWh
# Coefficients: {'hour': 1.23, 'day_of_week': -0.54, ...}
```

## 🔗 FastAPI Integration

### Example 1: Add to main.py

```python
from fastapi import FastAPI
from prediction_api import router as prediction_router

app = FastAPI(title="Smart Energy Platform")

# Include prediction endpoints
app.include_router(prediction_router)

# Other endpoints...
```

### Example 2: Train Model (cURL)

```bash
curl -X POST http://127.0.0.1:8000/prediction/train
```

**Response:**
```json
{
  "status": "success",
  "message": "Model trained on 1234 records",
  "training_metrics": {
    "r2_score": 0.8342,
    "mae": 2.31,
    "rmse": 3.45
  }
}
```

### Example 3: Get Forecast (cURL)

```bash
# 7-day forecast
curl http://127.0.0.1:8000/prediction/forecast/7

# 14-day forecast
curl http://127.0.0.1:8000/prediction/forecast/14

# 1-day forecast
curl http://127.0.0.1:8000/prediction/forecast/1
```

**Response:**
```json
{
  "daily_summary": [
    {
      "date": "2026-01-27",
      "day_name": "Monday",
      "total_kwh": 842.5,
      "average_kwh": 35.1,
      "peak_kwh": 52.3,
      "peak_hour": 14,
      "low_kwh": 18.2,
      "low_hour": 3
    }
  ]
}
```

### Example 4: Make Prediction (cURL)

```bash
# Friday 2pm
curl "http://127.0.0.1:8000/prediction/predict?year=2026&month=1&day=30&hour=14"

# Saturday midnight
curl "http://127.0.0.1:8000/prediction/predict?year=2026&month=1&day=31&hour=0"

# Tuesday 6am
curl "http://127.0.0.1:8000/prediction/predict?year=2026&month=1&day=28&hour=6"
```

**Response:**
```json
{
  "timestamp": "2026-01-30T14:00:00",
  "predicted_energy_kwh": 45.23,
  "readable_time": {
    "date": "Friday, January 30, 2026",
    "time": "02:00 PM",
    "is_weekend": false,
    "is_business_hour": true
  }
}
```

## 🐍 Python API Examples

### Example 1: Load Data from Database

```python
import pandas as pd
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import EnergyReading

# Get database session
db = SessionLocal()

# Query all energy readings
readings = db.query(EnergyReading).all()

# Convert to DataFrame
df = pd.DataFrame([
    {
        'timestamp': r.timestamp,
        'energy_consumed_kwh': r.energy_consumed_kwh
    }
    for r in readings
])

# Train model
predictor = EnergyConsumptionPredictor()
predictor.train(df)
```

### Example 2: Predict from Database Query

```python
from datetime import datetime
from energy_prediction_model import EnergyConsumptionPredictor

# Assume model is already trained (global variable in API)
# This is how it works in prediction_api.py

def predict_for_machine(machine_id: str, timestamp: datetime):
    """Predict energy for specific machine at specific time."""
    
    if not predictor.is_trained:
        raise Exception("Model must be trained first")
    
    prediction = predictor.predict(timestamp)
    
    return {
        'machine_id': machine_id,
        'timestamp': timestamp.isoformat(),
        'predicted_kwh': prediction['predicted_energy_kwh']
    }
```

### Example 3: Batch Predictions

```python
from datetime import datetime, timedelta
import pandas as pd

# Generate predictions for next 30 days
start = datetime.now()
end = start + timedelta(days=30)

forecast = predictor.predict_range(start, end, frequency='D')  # Daily

# Find peak day
peak_day = forecast.loc[forecast['predicted_energy_kwh'].idxmax()]
print(f"Peak consumption: {peak_day['predicted_energy_kwh']:.2f} kWh on {peak_day['timestamp']}")

# Find low day
low_day = forecast.loc[forecast['predicted_energy_kwh'].idxmin()]
print(f"Low consumption: {low_day['predicted_energy_kwh']:.2f} kWh on {low_day['timestamp']}")

# Calculate total
total = forecast['predicted_energy_kwh'].sum()
average = forecast['predicted_energy_kwh'].mean()
print(f"Total 30-day: {total:.2f} kWh")
print(f"Daily average: {average:.2f} kWh")
```

### Example 4: Visualize Forecast

```python
import matplotlib.pyplot as plt

# Get forecast data
forecast = predictor.predict_range(
    datetime(2026, 1, 27),
    datetime(2026, 2, 3),
    frequency='H'
)

# Plot
plt.figure(figsize=(14, 6))
plt.plot(forecast['timestamp'], forecast['predicted_energy_kwh'], linewidth=2)
plt.xlabel('Date & Time')
plt.ylabel('Energy (kWh)')
plt.title('7-Day Energy Forecast')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('forecast.png', dpi=100)
plt.show()

print("Saved to forecast.png")
```

## 🧪 Testing Examples

### Example 1: Unit Test

```python
import pytest
from energy_prediction_model import EnergyConsumptionPredictor
from datetime import datetime

def test_model_training():
    """Test that model trains successfully."""
    
    # Create sample data
    import pandas as pd
    df = pd.DataFrame({
        'timestamp': pd.date_range('2026-01-01', periods=100, freq='H'),
        'energy_consumed_kwh': [20 + i*0.5 for i in range(100)]
    })
    
    # Train model
    predictor = EnergyConsumptionPredictor()
    metrics = predictor.train(df)
    
    # Assertions
    assert predictor.is_trained
    assert metrics['r2_score'] > 0
    assert metrics['mae'] >= 0
    assert metrics['rmse'] >= 0
    assert len(metrics['coefficients']) == 6

def test_prediction_range():
    """Test that predictions are reasonable."""
    
    # Prediction should be positive
    start = datetime(2026, 1, 27)
    for hour in range(24):
        pred = predictor.predict(
            start.replace(hour=hour)
        )
        assert pred['predicted_energy_kwh'] > 0
        
        # Peak around 2pm
        if hour == 14:
            assert pred['predicted_energy_kwh'] > 40
        
        # Low around 3am
        if hour == 3:
            assert pred['predicted_energy_kwh'] < 30

def test_weekend_vs_weekday():
    """Test that weekends predict less than weekdays."""
    
    # Monday 2pm (weekday)
    monday = predictor.predict(datetime(2026, 1, 27, 14, 0))
    
    # Saturday 2pm (weekend)
    saturday = predictor.predict(datetime(2026, 2, 1, 14, 0))
    
    # Weekday should be higher
    assert monday['predicted_energy_kwh'] > saturday['predicted_energy_kwh']
```

### Example 2: Integration Test

```python
import requests

def test_prediction_api():
    """Test prediction API endpoints."""
    
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: Check status
    response = requests.get(f"{base_url}/prediction/model-status")
    assert response.status_code in [200, 400]  # OK or model not trained
    
    # Test 2: Train model
    response = requests.post(f"{base_url}/prediction/train")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    
    # Test 3: Check status (should now be trained)
    response = requests.get(f"{base_url}/prediction/model-status")
    assert response.status_code == 200
    data = response.json()
    assert data['is_trained'] is True
    
    # Test 4: Make prediction
    response = requests.get(
        f"{base_url}/prediction/predict",
        params={
            'year': 2026,
            'month': 1,
            'day': 27,
            'hour': 14
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert 'predicted_energy_kwh' in data
    assert data['predicted_energy_kwh'] > 0
    
    # Test 5: Get forecast
    response = requests.get(f"{base_url}/prediction/forecast/7")
    assert response.status_code == 200
    data = response.json()
    assert len(data['daily_summary']) == 7
    
    print("✅ All API tests passed!")
```

## 📊 Monitoring & Logging

### Example 1: Track Predictions

```python
import csv
from datetime import datetime

def log_prediction(timestamp, actual, predicted):
    """Log prediction for monitoring."""
    
    with open('predictions.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp.isoformat(),
            actual,
            predicted,
            abs(actual - predicted)  # Error
        ])

# Usage
actual_consumption = 45.2
prediction = predictor.predict(datetime.now())
log_prediction(
    datetime.now(),
    actual_consumption,
    prediction['predicted_energy_kwh']
)
```

### Example 2: Calculate Accuracy Over Time

```python
import pandas as pd

# Load logged predictions
df = pd.read_csv('predictions.csv', names=['timestamp', 'actual', 'predicted', 'error'])

# Calculate metrics
mae = df['error'].mean()
rmse = (df['error'] ** 2).mean() ** 0.5
mape = (df['error'] / df['actual']).mean() * 100

print(f"MAE: {mae:.2f} kWh")
print(f"RMSE: {rmse:.2f} kWh")
print(f"MAPE: {mape:.1f}%")

# Find worst prediction
worst = df.loc[df['error'].idxmax()]
print(f"Worst: {worst['error']:.2f} kWh error on {worst['timestamp']}")
```

## 🔄 Retraining Strategy

### Example 1: Weekly Retraining

```python
import schedule
import time
from datetime import datetime
from energy_prediction_model import EnergyConsumptionPredictor

# Global model
prediction_model = None

def retrain_model():
    """Retrain model with latest data."""
    global prediction_model
    
    db = SessionLocal()
    
    # Get all recent data (last 90 days)
    cutoff = datetime.now() - timedelta(days=90)
    readings = db.query(EnergyReading).filter(
        EnergyReading.timestamp >= cutoff
    ).all()
    
    # Convert to DataFrame
    df = pd.DataFrame([...])
    
    # Train new model
    new_model = EnergyConsumptionPredictor()
    metrics = new_model.train(df)
    
    # Check if better
    if metrics['r2_score'] > current_r2_score:
        prediction_model = new_model
        print(f"✅ Model retrained. R²: {metrics['r2_score']:.4f}")
    else:
        print(f"⚠️  New model not better. Keeping old model.")
    
    db.close()

# Schedule weekly retraining
schedule.every().monday.at("02:00").do(retrain_model)

# In main loop
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 2: A/B Testing

```python
from energy_prediction_model import EnergyConsumptionPredictor

# Train two models
model_v1 = EnergyConsumptionPredictor()
model_v1.train(data_old)

model_v2 = EnergyConsumptionPredictor()
model_v2.train(data_new)

# Test both
test_timestamp = datetime(2026, 1, 30, 14, 0)

pred_v1 = model_v1.predict(test_timestamp)
pred_v2 = model_v2.predict(test_timestamp)

print(f"V1 (old data): {pred_v1['predicted_energy_kwh']:.2f} kWh")
print(f"V2 (new data): {pred_v2['predicted_energy_kwh']:.2f} kWh")

# Compare metrics
print(f"V1 R²: {metrics_v1['r2_score']:.4f}")
print(f"V2 R²: {metrics_v2['r2_score']:.4f}")

# Use better one
if metrics_v2['r2_score'] > metrics_v1['r2_score']:
    best_model = model_v2
else:
    best_model = model_v1
```

## 🚀 Production Deployment

### Example: API with Caching

```python
from fastapi import FastAPI
from functools import lru_cache
from datetime import datetime, timedelta

app = FastAPI()
prediction_model = None
last_training = None

@lru_cache(maxsize=1000)
def get_cached_prediction(timestamp_str: str):
    """Cache predictions for same timestamp."""
    ts = datetime.fromisoformat(timestamp_str)
    pred = prediction_model.predict(ts)
    return pred

@app.get("/prediction/predict-cached")
def predict_with_cache(year: int, month: int, day: int, hour: int):
    """Predict with caching for performance."""
    
    timestamp = datetime(year, month, day, hour, 0)
    timestamp_str = timestamp.isoformat()
    
    result = get_cached_prediction(timestamp_str)
    return result

@app.post("/prediction/train-if-needed")
def auto_retrain():
    """Retrain only if data is old enough."""
    global last_training
    
    if last_training is None or \
       (datetime.now() - last_training) > timedelta(hours=24):
        # Retrain model
        metrics = prediction_model.train(get_recent_data())
        last_training = datetime.now()
        return {'status': 'retrained', 'metrics': metrics}
    else:
        return {'status': 'using cached model'}
```

---

## Quick Reference Card

```
BASIC USAGE
-----------
from energy_prediction_model import EnergyConsumptionPredictor
predictor = EnergyConsumptionPredictor()
predictor.train(data_df)
predictor.predict(datetime.now())

API ENDPOINTS
-----------
POST   /prediction/train              Train the model
GET    /prediction/forecast/{days}    Get forecast
GET    /prediction/predict             Single prediction
GET    /prediction/model-status        Check if trained
GET    /prediction/explain             Get explanation

METRICS
-------
R² Score:  0-1 range (higher is better)
MAE:       Average error in kWh (lower is better)
RMSE:      Penalized error in kWh (lower is better)

FEATURES USED
-------------
hour, day_of_week, day_of_month, month, is_weekend, is_business_hour
```

---

**Version:** 1.0
**Created:** January 27, 2026
**Status:** ✅ Complete
