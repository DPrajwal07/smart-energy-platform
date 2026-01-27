# Energy Prediction Integration Guide

## ✅ Integration Complete

The energy prediction model has been successfully integrated into your FastAPI application with **3 new endpoints**.

---

## 🎯 New Endpoints

### 1. POST /prediction/train
**Purpose:** Train the Linear Regression model

```bash
curl -X POST http://127.0.0.1:8000/prediction/train
```

**Response:**
```json
{
  "status": "success",
  "message": "Model trained on 1234 records",
  "is_trained": true,
  "r2_score": 0.8342,
  "mae": 2.31,
  "rmse": 3.45,
  "training_timestamp": "2026-01-27T10:30:00"
}
```

**What it does:**
- Queries all historical energy data from database
- Trains Linear Regression model on time-based features
- Returns accuracy metrics (R², MAE, RMSE)
- Caches model for future predictions

**Requirements:**
- Need at least 100 energy readings in database
- Database must be running
- Data must have valid timestamps

---

### 2. GET /prediction/next-7-days
**Purpose:** Get 7-day energy consumption forecast (hourly)

```bash
curl http://127.0.0.1:8000/prediction/next-7-days
```

**Response:**
```json
{
  "status": "success",
  "forecast_days": 7,
  "generated_at": "2026-01-27T10:30:00",
  "forecast_period": {
    "start": "2026-01-27T10:30:00",
    "end": "2026-02-03T10:30:00"
  },
  "summary": {
    "total_kwh": 5945.8,
    "average_daily_kwh": 849.4,
    "peak_day": "2026-01-30",
    "peak_day_kwh": 875.3
  },
  "daily_summary": [
    {
      "date": "2026-01-27",
      "day_name": "Monday",
      "total_kwh": 842.5,
      "average_kwh": 35.1,
      "peak_kwh": 52.3,
      "peak_hour": 14,
      "low_kwh": 18.2,
      "low_hour": 3,
      "hourly_count": 24
    },
    {
      "date": "2026-01-28",
      "day_name": "Tuesday",
      "total_kwh": 850.2,
      "average_kwh": 35.4,
      "peak_kwh": 53.1,
      "peak_hour": 14,
      "low_kwh": 17.8,
      "low_hour": 2,
      "hourly_count": 24
    }
    // ... 5 more days
  ]
}
```

**What it does:**
- Generates hourly predictions for next 7 days
- Organizes by day with hourly and daily summaries
- Shows peak and low hours
- Returns total and average consumption

**Requirements:**
- Model must be trained first (call /prediction/train)
- Returns 168 hourly predictions (24 hours × 7 days)

---

### 3. GET /prediction/status
**Purpose:** Check if model is trained and ready

```bash
curl http://127.0.0.1:8000/prediction/status
```

**Response (Trained):**
```json
{
  "is_trained": true,
  "model_type": "Linear Regression",
  "features": 6,
  "feature_names": [
    "hour",
    "day_of_week",
    "day_of_month",
    "month",
    "is_weekend",
    "is_business_hour"
  ],
  "message": "Model ready for predictions"
}
```

**Response (Not Trained):**
```json
{
  "is_trained": false,
  "model_type": "Linear Regression",
  "features": 6,
  "message": "Model not trained. Call POST /prediction/train first"
}
```

---

## 🚀 Quick Start

### Step 1: Add Sample Energy Data (if needed)
```bash
# Add a few days of hourly data
for i in {0..23}; do
  curl -X POST http://127.0.0.1:8000/energy/add \
    -H "Content-Type: application/json" \
    -d "{
      \"machine_id\": \"TEST-PUMP\",
      \"power_kw\": 50,
      \"energy_consumed_kwh\": 1
    }"
done
```

### Step 2: Check Model Status
```bash
curl http://127.0.0.1:8000/prediction/status
```

### Step 3: Train the Model
```bash
curl -X POST http://127.0.0.1:8000/prediction/train
```

Expected output: `"is_trained": true`

### Step 4: Get 7-Day Forecast
```bash
curl http://127.0.0.1:8000/prediction/next-7-days
```

### Step 5: Verify Results
- Check `summary.total_kwh` (should be realistic)
- Check `daily_summary[0].peak_hour` (should be 14, peak time)
- Check if weekend days have lower totals

---

## 📊 Understanding the Response

### Daily Summary Fields

| Field | Example | Meaning |
|-------|---------|---------|
| `date` | 2026-01-27 | Date of prediction |
| `day_name` | Monday | Day of the week |
| `total_kwh` | 842.5 | Total energy for that day |
| `average_kwh` | 35.1 | Average per hour |
| `peak_kwh` | 52.3 | Highest hour |
| `peak_hour` | 14 | Hour with highest consumption (2pm) |
| `low_kwh` | 18.2 | Lowest hour |
| `low_hour` | 3 | Hour with lowest consumption (3am) |
| `hourly_count` | 24 | Number of hourly predictions |

### Typical Patterns in Predictions

```
Peak Hour (2pm): ~50 kWh
Afternoon: ~45 kWh
Morning: ~30 kWh
Night: ~18 kWh
Weekday: ~40 kWh average
Weekend: ~30 kWh average
```

---

## 🧪 Testing the Integration

### Test 1: Check Status
```bash
curl http://127.0.0.1:8000/prediction/status
# Should show: "is_trained": false (before training)
```

### Test 2: Train Model
```bash
curl -X POST http://127.0.0.1:8000/prediction/train
# Should show: "is_trained": true
```

### Test 3: Check Status Again
```bash
curl http://127.0.0.1:8000/prediction/status
# Should now show: "is_trained": true
```

### Test 4: Get Forecast
```bash
curl http://127.0.0.1:8000/prediction/next-7-days
# Should show 7 days of predictions with summaries
```

### Test 5: Verify Swagger UI
```
http://127.0.0.1:8000/docs
```
Look for "Energy Prediction Endpoints" section - all 3 endpoints should be listed.

---

## 💡 How It Works

### The Model
- **Type:** Linear Regression (simple, fast, interpretable)
- **Features:** 6 time-based (hour, day, month, etc.)
- **Formula:** Energy = Base + (Hour × Weight₁) + (Day × Weight₂) + ...

### Prediction Process
1. **Extract features** from current/future timestamps
2. **Apply learned formula** to calculate energy
3. **Return prediction** as kWh

### Example Calculation
```
Friday 2pm prediction:

Base energy: 22 kWh
Hour (14): 14 × 1.23 = +17.2 kWh
Day (4): 4 × -0.54 = -2.2 kWh
Is weekend (0): 0 × -1.54 = 0 kWh
Business hour (1): 1 × 2.34 = +2.3 kWh

Total: 22 + 17.2 - 2.2 + 0 + 2.3 = 39.3 kWh
```

---

## ⚙️ Technical Details

### Code Location
- **Endpoints:** main.py (lines ~835-1050)
- **Model:** energy_prediction_model.py
- **Features:** hour, day_of_week, day_of_month, month, is_weekend, is_business_hour

### Global Variables
```python
prediction_model = None      # Cached model instance
model_is_trained = False     # Training status flag
```

### Error Handling
- Returns **400** if model not trained
- Returns **400** if insufficient data (< 100 records)
- Returns **500** for unexpected errors

### JSON Response Format
All endpoints return consistent JSON:
```json
{
  "status": "success|error",
  "data": { ... },
  "timestamp": "2026-01-27T10:30:00"
}
```

---

## 🔍 API Documentation in Swagger UI

When you start the server, visit:
```
http://127.0.0.1:8000/docs
```

You'll see all 3 new endpoints with:
- Full docstring descriptions
- Parameter documentation
- Example responses
- Try It Out button to test directly

---

## 🐛 Troubleshooting

### Error: "Model not trained"
```
Solution: POST /prediction/train first
```

### Error: "Insufficient data"
```
Solution: Need 100+ records in database
Add more energy readings via /energy/add
```

### Error: "No module named 'energy_prediction_model'"
```
Solution: Ensure energy_prediction_model.py is in same directory as main.py
```

### Predictions seem wrong
```
Checklist:
1. Check model status: GET /prediction/status (should be trained)
2. Verify data range: Check timestamps are recent
3. Retrain model: POST /prediction/train
4. Check for outliers in raw data
```

---

## 📈 Example: Using Forecast in Dashboard

```python
# Get forecast
import requests
response = requests.get('http://127.0.0.1:8000/prediction/next-7-days')
forecast = response.json()

# Extract daily data
daily = forecast['daily_summary']

# Find peak consumption day
peak_day = max(daily, key=lambda x: x['total_kwh'])
print(f"Peak: {peak_day['date']} ({peak_day['day_name']}) = {peak_day['total_kwh']} kWh")

# Calculate average
avg = sum(d['total_kwh'] for d in daily) / len(daily)
print(f"Average daily: {avg:.1f} kWh")

# Identify weekend
weekends = [d for d in daily if d['day_name'] in ['Saturday', 'Sunday']]
weekend_avg = sum(d['total_kwh'] for d in weekends) / len(weekends)
print(f"Weekend average: {weekend_avg:.1f} kWh")
```

---

## 🎯 Integration Checklist

- [x] Import energy_prediction_model
- [x] Import timedelta
- [x] Add global variables (prediction_model, model_is_trained)
- [x] Add POST /prediction/train endpoint
- [x] Add GET /prediction/next-7-days endpoint (MAIN)
- [x] Add GET /prediction/status endpoint
- [x] Add comprehensive docstrings
- [x] Add error handling (400, 500)
- [x] Format JSON responses cleanly
- [x] Cache model in memory

---

## 📚 Files Reference

| File | Purpose |
|------|---------|
| **main.py** | FastAPI app with 3 new endpoints |
| **energy_prediction_model.py** | Core ML model |
| **PREDICTION_INTEGRATION_GUIDE.md** | This file |

---

## ✨ Features

✅ **Clean Code** - Well-commented, easy to understand
✅ **RESTful** - Follows REST conventions
✅ **Error Handling** - Comprehensive error messages
✅ **Caching** - Model cached in memory for performance
✅ **Documentation** - Full docstrings for all endpoints
✅ **JSON Response** - Clean, readable JSON format
✅ **Swagger Support** - Auto-documented in /docs

---

## 🚀 Next Steps

1. **Start the server:** `python main.py`
2. **Visit API docs:** http://127.0.0.1:8000/docs
3. **Train the model:** POST /prediction/train
4. **Get forecast:** GET /prediction/next-7-days
5. **Integrate in UI:** Use forecast data in dashboard
6. **Monitor accuracy:** Track predictions vs actual usage
7. **Retrain periodically:** Add new data and retrain

---

**Status:** ✅ Complete and integrated
**Ready to use:** Yes
**All requirements met:** Yes

Start your server and try it out! 🎉
