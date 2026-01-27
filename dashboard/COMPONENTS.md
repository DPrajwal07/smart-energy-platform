# Dashboard Components Guide

This guide explains each component in the React dashboard and how they work together.

## Component Hierarchy

```
App (Root)
└── Dashboard (Main Container)
    ├── Dashboard Header (Title + Train Button)
    ├── Summary Cards Section
    │   ├── EnergyCard (Total Energy)
    │   ├── EnergyCard (Average Usage)
    │   ├── EnergyCard (Latest Reading)
    │   └── EnergyCard (Carbon Emissions)
    ├── Charts Section
    │   ├── EnergyChart (Historical Usage)
    │   └── ForecastChart (7-Day Forecast)
    └── Status Section
        └── StatusCard (Model Status, Data Points, etc.)
```

## Component Details

### 1. App Component (`src/App.js`)

**Purpose:** Root component of the entire application

**Responsibility:** 
- Renders the Dashboard component
- Provides top-level styling wrapper

**Code:**
```javascript
function App() {
  return (
    <div className="app">
      <Dashboard />
    </div>
  );
}
```

**When to modify:** Rarely - this is just the entry point

---

### 2. Dashboard Component (`src/Dashboard.js`)

**Purpose:** Main orchestrator component that manages all dashboard state and data

**Key Features:**
- ✅ Fetches data from FastAPI backend
- ✅ Manages loading and error states
- ✅ Auto-refreshes data every 30 seconds
- ✅ Handles model training
- ✅ Calculates summary statistics

**State Variables:**

| State | Purpose | Type |
|-------|---------|------|
| `energyReadings` | All energy consumption data | Array |
| `forecast` | 7-day predictions | Object |
| `modelStatus` | Model training status | Object |
| `carbonData` | CO2 emissions data | Object |
| `loading` | Data loading status | Boolean |
| `error` | Error messages | String |
| `trainLoading` | Model training status | Boolean |

**Main Functions:**

```javascript
// Fetches all dashboard data from API
const fetchDashboardData = async () { ... }

// Handles model training
const handleTrainModel = async () { ... }
```

**Flow:**
1. Component mounts → useEffect runs
2. `fetchDashboardData()` fetches from API
3. Sets state with data
4. Auto-refresh every 30 seconds
5. User clicks "Train Model" → calls `handleTrainModel()`

**When to modify:**
- Adding new data sources
- Changing refresh interval
- Adding new functionality

---

### 3. EnergyChart Component (`src/components/EnergyChart.js`)

**Purpose:** Displays historical energy consumption as a line chart

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `data` | Array | ✅ Yes | Energy readings with `timestamp` and `energy_consumed_kwh` |

**What it does:**
- Takes energy readings from props
- Formats timestamps for display
- Renders interactive line chart using Recharts
- Shows consumption over time

**Chart Details:**
- **X-Axis:** Date of reading
- **Y-Axis:** Energy consumption (kWh)
- **Line:** Blue, interactive with hover points
- **Tooltip:** Shows exact date and consumption on hover

**Example Usage:**
```javascript
<EnergyChart data={energyReadings} />
```

**Data Format Expected:**
```javascript
[
  { timestamp: "2024-01-15T10:00:00", energy_consumed_kwh: 45.5 },
  { timestamp: "2024-01-15T11:00:00", energy_consumed_kwh: 48.2 },
  // ... more readings
]
```

---

### 4. ForecastChart Component (`src/components/ForecastChart.js`)

**Purpose:** Displays 7-day energy consumption predictions as a bar chart

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `data` | Object | ✅ Yes | Forecast object with `predictions` array |

**What it does:**
- Takes hourly predictions from model
- Groups them by day and calculates daily average
- Renders bar chart showing daily predictions
- Helps plan energy usage

**Chart Details:**
- **X-Axis:** Date (next 7 days)
- **Y-Axis:** Predicted energy consumption (kWh)
- **Bars:** Green, representing predictions
- **Tooltip:** Shows daily average prediction on hover

**Example Usage:**
```javascript
<ForecastChart data={forecast} />
```

**Data Format Expected:**
```javascript
{
  predictions: [
    { timestamp: "2024-01-16T00:00:00", predicted_consumption: 45.2 },
    { timestamp: "2024-01-16T01:00:00", predicted_consumption: 42.8 },
    // ... more hourly predictions
  ],
  summary: {
    total_kwh: 3200
  }
}
```

---

### 5. EnergyCard Component (`src/components/EnergyCard.js`)

**Purpose:** Displays a single metric in an attractive card format

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `title` | String | ✅ Yes | Card title/label |
| `value` | String/Number | ✅ Yes | The metric value |
| `unit` | String | ✅ Yes | Unit of measurement |
| `icon` | String | ✅ Yes | Emoji icon |
| `color` | String | ❌ No | Color theme (primary, secondary, success, warning) |

**What it does:**
- Displays a metric with icon and styling
- Shows title, value, and unit
- Has hover animation effect
- Color-coded for different metric types

**Available Colors:**
- `primary` (purple) - Main metrics
- `secondary` (dark purple) - Alternative metrics
- `success` (green) - Positive metrics
- `warning` (yellow) - Attention needed

**Example Usage:**
```javascript
<EnergyCard
  title="Total Energy"
  value={1234.56}
  unit="kWh"
  icon="⚡"
  color="primary"
/>
```

**Visual Layout:**
```
[Icon] Title
       123.45 kWh
```

---

### 6. StatusCard Component (`src/components/StatusCard.js`)

**Purpose:** Displays system status information

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `title` | String | ✅ Yes | Status item title |
| `status` | String/Number | ✅ Yes | Main status value |
| `details` | String | ✅ Yes | Additional description |
| `icon` | String | ✅ Yes | Emoji icon |

**What it does:**
- Shows system status in structured format
- Displays model training status, data availability, etc.
- Provides additional context with details text
- Visual feedback with icons

**Example Usage:**
```javascript
<StatusCard
  title="Prediction Model"
  status={modelStatus?.is_trained ? 'Ready' : 'Not Trained'}
  details="Features: 10"
  icon="✓"
/>
```

**Visual Layout:**
```
[Icon] Title
       Status Value
       Details text
```

---

## Data Flow Diagram

```
App Component
    ↓
Dashboard Component
    ├─→ useEffect (on mount)
    │   └─→ fetchDashboardData()
    │       ├─→ API: getEnergyReadings()
    │       ├─→ API: getPredictionStatus()
    │       ├─→ API: getForecast()
    │       └─→ API: getCarbonAnalysis()
    │
    ├─→ Renders: Summary Cards
    │   └─→ EnergyCard × 4
    │
    ├─→ Renders: Charts
    │   ├─→ EnergyChart (uses energyReadings state)
    │   └─→ ForecastChart (uses forecast state)
    │
    └─→ Renders: Status Section
        └─→ StatusCard × 3
```

## State Management Pattern

The dashboard uses React's `useState` and `useEffect` hooks:

**Example:**
```javascript
// Create state variable
const [energyReadings, setEnergyReadings] = useState([]);

// Update state (re-renders component)
setEnergyReadings(data);

// Use in component
<EnergyChart data={energyReadings} />
```

**Key Pattern:**
1. Initialize state with `useState()`
2. Fetch data with `useEffect()`
3. Update state with setter function
4. Components re-render automatically
5. Pass state as props to child components

## Event Handling

### Training Model

```javascript
// Button click handler
const handleTrainModel = async () => {
  setTrainLoading(true);  // Show loading state
  
  try {
    await trainPredictionModel();  // API call
    // Refresh status after training
    const status = await getPredictionStatus();
    setModelStatus(status);
  } catch (err) {
    setError('Failed to train model');
  }
  
  setTrainLoading(false);  // Hide loading state
};
```

## Error Handling Pattern

All API calls use try-catch:

```javascript
try {
  const data = await apiFunction();
  setData(data);  // Success
} catch (error) {
  setError('User-friendly error message');
  console.error(error);  // Log for debugging
}
```

## Performance Optimization

**Auto-refresh (every 30 seconds):**
```javascript
useEffect(() => {
  fetchDashboardData();
  
  // Set up interval
  const interval = setInterval(fetchDashboardData, 30000);
  
  // Clean up on unmount
  return () => clearInterval(interval);
}, []);
```

## Customization Examples

### Change Chart Colors

Edit `EnergyChart.js`:
```javascript
<Line
  stroke="#YOUR_COLOR"  // Change line color
  fill="YOUR_COLOR"     // Change fill color
/>
```

### Add New Card

In `Dashboard.js`:
```javascript
<EnergyCard
  title="Peak Usage"
  value={maxEnergy}
  unit="kWh"
  icon="📊"
  color="warning"
/>
```

### Change Refresh Interval

In `Dashboard.js`:
```javascript
const interval = setInterval(fetchDashboardData, 60000); // 60 seconds instead of 30
```

## Testing Tips

1. **Check console for errors:** Open DevTools (F12) → Console tab
2. **Verify API calls:** Network tab → Check API requests
3. **Test loading states:** Slow down network in DevTools
4. **Test error handling:** Stop the API backend temporarily
5. **Check responsive design:** Resize browser or use mobile view

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No data to display" | API not returning data | Check backend is running |
| Charts empty | Wrong data format | Verify API response structure |
| Model status shows "Not Trained" | Model needs training | Click "Train Model" button |
| API Connection Error | Backend offline | Start FastAPI backend |

---

**Need help?** Check the code comments and JSDoc blocks in each component!
