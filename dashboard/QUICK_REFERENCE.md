# ⚡ Smart Energy Dashboard - Quick Reference Card

*Keep this handy while developing!*

---

## 🚀 Getting Started (Copy & Paste)

```bash
# Setup
cd dashboard
npm install

# Run
npm start

# Build for production
npm run build
```

**Result:** Dashboard opens at http://localhost:3000 ✅

---

## 📁 Key Files at a Glance

| File | What It Does | Where |
|------|-------------|-------|
| **Dashboard.js** | Main component, manages all state | `src/` |
| **api.js** | 8 API functions | `src/services/` |
| **EnergyChart.js** | Historical chart | `src/components/` |
| **ForecastChart.js** | Prediction chart | `src/components/` |
| **package.json** | Dependencies | root |

---

## 🎨 Colors to Customize

Edit these in `src/index.css`:

```css
Primary Purple:    #667eea  (header, main accent)
Secondary Purple:  #764ba2  (alternate accent)
Success Green:     #4CAF50  (positive metrics)
Warning Yellow:    #FFC107  (alerts)
Light Gray:        #e0e0e0  (borders)
```

---

## 🔧 Common Modifications

### Change API URL
**File:** `src/services/api.js`

```javascript
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // ← Change this
});
```

### Add New Card
**File:** `src/Dashboard.js`

```javascript
<EnergyCard
  title="Your Title"
  value={yourValue}
  unit="kWh"
  icon="⚡"
  color="primary"
/>
```

### Change Refresh Interval
**File:** `src/Dashboard.js`

```javascript
const interval = setInterval(fetchDashboardData, 30000);  // ← Change 30000 (ms)
// 60000 = 60 seconds, 10000 = 10 seconds
```

---

## 📊 Component Props Reference

### EnergyCard Props
```javascript
<EnergyCard
  title="Text"                    // Required: Card title
  value={123.45}                  // Required: Metric value
  unit="kWh"                      // Required: Unit name
  icon="⚡"                        // Required: Emoji icon
  color="primary|secondary|success|warning"  // Optional: Color theme
/>
```

### StatusCard Props
```javascript
<StatusCard
  title="Model Status"            // Required: Card title
  status="Ready"                  // Required: Status value
  details="Training complete"     // Required: Additional info
  icon="✓"                        // Required: Emoji icon
/>
```

### EnergyChart Props
```javascript
<EnergyChart
  data={energyReadings}           // Required: Array of readings
/>
// Expected format:
// [{ timestamp: "2024-01-15T10:00:00", energy_consumed_kwh: 45.5 }, ...]
```

### ForecastChart Props
```javascript
<ForecastChart
  data={forecast}                 // Required: Forecast object
/>
// Expected format:
// { predictions: [{ timestamp: "...", predicted_consumption: 45.2 }, ...] }
```

---

## 🔌 API Functions (8 Total)

| Function | Returns | Throws |
|----------|---------|--------|
| `getEnergyReadings()` | Array of readings | Error on failure |
| `addEnergyReading(data)` | New reading object | Error on failure |
| `trainPredictionModel()` | Status object | Error on failure |
| `getForecast()` | Forecast object | Error on failure |
| `getPredictionStatus()` | Status with is_trained | Error on failure |
| `getCarbonAnalysis()` | Carbon data | Error on failure |
| `getDailyConsumption()` | Daily stats | Error on failure |
| `healthCheck()` | Health status | Error on failure |

**Usage Example:**
```javascript
try {
  const forecast = await getForecast();
  setForecast(forecast);
} catch (error) {
  setError('Failed to fetch forecast');
}
```

---

## 🧠 State Variables in Dashboard

```javascript
const [energyReadings, setEnergyReadings] = useState([]);    // Energy data
const [forecast, setForecast] = useState(null);              // Predictions
const [modelStatus, setModelStatus] = useState(null);        // Model state
const [carbonData, setCarbonData] = useState(null);          // CO2 emissions
const [loading, setLoading] = useState(true);                // Loading flag
const [error, setError] = useState(null);                    // Error message
const [trainLoading, setTrainLoading] = useState(false);     // Train flag
```

---

## 🎨 CSS Classes Available

### Cards
```html
<div class="energy-card primary|secondary|success|warning">
  <div class="card-icon">⚡</div>
  <div class="card-content">
    <h3 class="card-title">Title</h3>
    <div class="card-value">
      <span class="value">123</span>
      <span class="unit">kWh</span>
    </div>
  </div>
</div>
```

### Status Indicator
```html
<span class="status-indicator active|inactive">
  ✓ Model Ready
</span>
```

### Buttons
```html
<button class="btn btn-primary|btn-secondary">
  Click me
</button>

<!-- Loading state -->
<button class="btn btn-primary loading" disabled>
  ⏳ Training...
</button>
```

---

## 📱 Responsive Design Breakpoints

```css
/* Mobile: < 768px */
@media (max-width: 768px) {
  /* Mobile styles here */
}

/* Tablet: 768px - 1199px */
@media (max-width: 1199px) {
  /* Tablet styles here */
}

/* Desktop: 1200px+ */
/* Default/desktop styles */
```

---

## 🐛 Debugging Tips

### Check State in Console
```javascript
// Add to Dashboard.js
useEffect(() => {
  console.log('Energy readings:', energyReadings);
  console.log('Forecast:', forecast);
  console.log('Model status:', modelStatus);
}, [energyReadings, forecast, modelStatus]);
```

### Log API Responses
```javascript
const readings = await getEnergyReadings();
console.log('API Response:', readings);
```

### Check Network Requests
1. Open DevTools (F12)
2. Go to "Network" tab
3. Make API call
4. Click request to see details

### View Errors in Console
```bash
DevTools → Console tab → Look for errors
```

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Failed to fetch data" | Backend not running. Run `python main.py` |
| Port 3000 in use | Run `PORT=3001 npm start` |
| Blank page | Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac) |
| Charts empty | Train model first (click "Train Model" button) |
| No npm modules | Run `npm install` in dashboard folder |
| Old code still showing | Clear browser cache or hard refresh |

---

## 📚 Documentation Quick Links

| Need | Link |
|------|------|
| Setup in 5 min | [QUICKSTART.md](QUICKSTART.md) |
| What's included? | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Full docs | [README.md](README.md) |
| System design | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Component details | [COMPONENTS.md](COMPONENTS.md) |
| Dev tips | [DEVELOPMENT.md](DEVELOPMENT.md) |
| Navigation | [INDEX.md](INDEX.md) |

---

## 🎯 File Sizes & Complexity

| File | Lines | Complexity | Importance |
|------|-------|-----------|-----------|
| Dashboard.js | 250+ | ⭐⭐⭐⭐ | CRITICAL |
| api.js | 150+ | ⭐⭐⭐ | CRITICAL |
| EnergyChart.js | 40 | ⭐⭐ | Important |
| ForecastChart.js | 50 | ⭐⭐ | Important |
| EnergyCard.js | 30 | ⭐ | Standard |
| StatusCard.js | 30 | ⭐ | Standard |
| App.js | 5 | ⭐ | Simple |
| index.js | 10 | ⭐ | Simple |

---

## 🚀 Deployment Steps

### Build
```bash
cd dashboard
npm run build
```

### Vercel (Easiest)
1. Connect GitHub repo
2. Click "Deploy"
3. Done! ✅

### Netlify
```bash
npm run build
# Drag build/ folder to Netlify
```

### Traditional Server
```bash
npm run build
# Copy build/ to server
# Configure web server to serve static files
```

---

## 🎓 Code Style Guide

### Naming
```javascript
// Good names
const energyReadings = [];
const averageConsumption = 45.5;
const isModelTrained = true;

// Avoid
const data = [];
const val = 45.5;
const flag = true;
```

### Commenting
```javascript
// Good: explains WHY
// Calculate average to show user's typical usage
const average = total / count;

// Bad: explains WHAT (code already does that)
// Set average
const avg = tot / cnt;
```

### Functions
```javascript
// Good: JSDoc + clear purpose
/**
 * Fetches energy readings from API
 * @returns {Promise<Array>} Array of readings
 * @throws {Error} If API fails
 */
async function getReadings() { ... }

// Bad: no docs, unclear
async function get() { ... }
```

---

## 📊 Project Metrics

```
Files Created:         22
Lines of Code:      1,500+
Components:            6
API Functions:         8
CSS Stylesheets:       5
Documentation:    2,500+ lines
Setup Time:        5 minutes
Deploy Time:       5 minutes
```

---

## ✅ Success Checklist

- [ ] Dashboard runs without errors
- [ ] No errors in browser console (F12)
- [ ] Charts display data
- [ ] "Train Model" button works
- [ ] Status shows "✓ Model Ready"
- [ ] Data refreshes every 30 seconds
- [ ] Works on mobile (try different sizes)
- [ ] All links work
- [ ] No 404 errors

---

## 🔒 Security Checklist

- ✅ No API keys in code
- ✅ No passwords exposed
- ✅ Error messages are generic
- ✅ Input validation on backend
- ✅ HTTPS ready for production

---

## 📞 Need Help?

1. **Check code comments** - Every function has JSDoc
2. **Read documentation** - 7 comprehensive guides
3. **Browse examples** - Components show patterns
4. **Check browser console** - Error messages are helpful
5. **Review architecture** - ARCHITECTURE.md explains design

---

## 🎯 Your Quick Workflow

```
1. cd dashboard
   ↓
2. npm install
   ↓
3. npm start
   ↓
4. Browser opens → Dashboard at http://localhost:3000
   ↓
5. Click "Train Model"
   ↓
6. See charts populate ✅
   ↓
7. Ready to customize!
```

---

## 🌟 Key Reminders

- 🔄 **Data refreshes** every 30 seconds automatically
- 🎨 **Colors customizable** in CSS files
- 🔧 **Easy to extend** - component-based design
- 📱 **Mobile friendly** - responsive grid
- 📚 **Well documented** - code + 7 guides
- ⚡ **Production ready** - no known issues
- 🚀 **Easy to deploy** - build & upload

---

## 📋 Bookmarks

Save these for quick reference:

- **Setup:** QUICKSTART.md
- **Components:** COMPONENTS.md  
- **Debugging:** DEVELOPMENT.md
- **Architecture:** ARCHITECTURE.md
- **Full Docs:** README.md

---

*Happy coding! 💻✨*

**Last Updated:** Today  
**Status:** ✅ Complete  
**Version:** 1.0.0
