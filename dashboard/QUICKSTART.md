# Quick Start Guide - Smart Energy Dashboard

Get your dashboard up and running in 5 minutes! 🚀

## ⏱️ 5-Minute Setup

### Step 1: Prerequisites Check (30 seconds)

Make sure you have:
- ✅ Node.js installed (v14+)
- ✅ FastAPI backend running on `http://127.0.0.1:8000`

**Check Node.js:**
```bash
node --version
npm --version
```

**Start your FastAPI backend** (in a separate terminal):
```bash
cd ..  # Go to parent directory
python main.py
# Should see: "Uvicorn running on http://127.0.0.1:8000"
```

### Step 2: Install Dependencies (2 minutes)

```bash
cd dashboard
npm install
```

This downloads React, Recharts, Axios, and other dependencies.

### Step 3: Start Development Server (1 minute)

```bash
npm start
```

Your browser will automatically open to:
```
http://localhost:3000
```

### Step 4: Verify Everything Works (1 minute)

You should see:
- ✅ "Smart Energy Platform" header
- ✅ "Train Model" button (top right)
- ✅ Loading spinner while fetching data

If you see an error:
1. Check backend is running on port 8000
2. Check browser console (F12) for error messages
3. See troubleshooting section below

## 🎯 First Steps to Try

### 1. Train the Model (30 seconds)

1. Click **"Train Model"** button (top right)
2. Wait for button to show "✓ Model Ready"
3. You should see charts populate with data

### 2. Explore the Dashboard

- **⚡ Summary Cards** (top): Total energy, average usage, latest reading, emissions
- **📈 Energy Chart** (middle left): Historical energy consumption
- **🔮 Forecast Chart** (middle right): 7-day predictions
- **📋 Status Cards** (bottom): System status and statistics

### 3. Check the Model Status

Look for the indicator next to "Train Model":
- 🟢 **"✓ Model Ready"** = Predictions working
- 🔴 **"○ Model Not Ready"** = Need to train first

## 📁 File Structure Explained

```
dashboard/
├── src/
│   ├── Dashboard.js          ← Main dashboard (50% of code)
│   ├── App.js                ← Root component
│   ├── components/           ← Reusable components
│   │   ├── EnergyChart.js    ← Historical usage chart
│   │   ├── ForecastChart.js  ← Prediction chart
│   │   ├── EnergyCard.js     ← Metric cards
│   │   └── StatusCard.js     ← Status display
│   └── services/
│       └── api.js            ← API calls (talks to backend)
├── package.json              ← Dependencies
└── README.md                 ← Full documentation
```

## 🔧 Common Tasks

### Change the API URL

If your backend runs on a different address, edit `src/services/api.js`:

```javascript
// Find this line:
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // ← Change here
});
```

### Add More Energy Readings

You need data in the backend database. Use the API endpoint:

```bash
curl -X POST http://127.0.0.1:8000/energy/add \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "meter-1",
    "energy_consumed_kwh": 45.5,
    "timestamp": "2024-01-15T10:00:00"
  }'
```

### Make the Page Wider

The dashboard is responsive. Try:
1. Resize your browser window
2. Open DevTools → Click mobile icon
3. Toggle between different screen sizes

## 🐛 Troubleshooting

### Problem: "Failed to fetch dashboard data"

**Cause:** Backend not running

**Solution:**
```bash
# Check if backend is running
curl http://127.0.0.1:8000/health

# If not, start it (in new terminal):
cd ..
python main.py
```

### Problem: "Port 3000 already in use"

**Cause:** Another app using port 3000

**Solution:**
```bash
# Use a different port
PORT=3001 npm start
```

### Problem: Blank page with no errors

**Cause:** React not loading

**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Clear cache: Delete `node_modules/` and run `npm install` again
3. Check console: Press `F12` → Console tab

### Problem: "Cannot find module 'recharts'"

**Cause:** Dependencies not installed

**Solution:**
```bash
npm install
```

### Problem: Charts empty but no errors

**Cause:** No data in database

**Solution:**
1. Click "Train Model" button
2. Wait for model training to complete
3. Check backend API: `curl http://127.0.0.1:8000/energy/readings`

## 💡 Code Examples

### Looking at API responses

Edit `src/Dashboard.js`, find `fetchDashboardData`:

```javascript
const readings = await getEnergyReadings();
console.log('Energy readings:', readings);  // ← Add this line
setEnergyReadings(readings || []);
```

Then open browser console (F12) to see the data.

### Adding a console log to see state changes

In any component:
```javascript
useEffect(() => {
  console.log('Component mounted');
  console.log('Energy readings:', energyReadings);
}, [energyReadings]);
```

### Testing a single API call

```bash
# In browser console:
import { getForecast } from './services/api.js'
const forecast = await getForecast()
console.log(forecast)
```

## 📚 Learning Resources

**Start Here (15 min read):**
- [React Basics](https://react.dev/learn)
- [Understanding useState](https://react.dev/reference/react/useState)
- [Understanding useEffect](https://react.dev/reference/react/useEffect)

**Chart Library:**
- [Recharts Tutorial](https://recharts.org/en-US/guide)
- [Common Recharts Examples](https://recharts.org/en-US/examples)

**API Communication:**
- [Axios Guide](https://axios-http.com)
- [Async/Await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous)

## ✅ Checklist for Success

- [ ] Node.js installed
- [ ] Backend running on port 8000
- [ ] `npm install` completed
- [ ] `npm start` running (no errors)
- [ ] Dashboard visible at http://localhost:3000
- [ ] "Train Model" button works
- [ ] Charts display data
- [ ] Status shows "✓ Model Ready"

## 🎉 What's Next?

### Short-term (Today)
- Explore the dashboard UI
- Check different screen sizes
- Click "Train Model" and see forecasts update

### Medium-term (This week)
- Read the component documentation (COMPONENTS.md)
- Try modifying the styling
- Understand how API calls work (api.js)

### Long-term (This month)
- Add new features (custom chart, alerts, etc.)
- Deploy to production
- Integrate with other systems

## 🚀 Deployment

### Deploy locally (your machine)

Already running! Access at: `http://localhost:3000`

### Deploy to free hosting

**Option 1: Vercel (Easiest)**
1. Connect GitHub repository
2. Click "Deploy"
3. Done! (automatic deployments)

**Option 2: Netlify**
```bash
npm run build
# Drag build/ folder to Netlify
```

### Production Build

```bash
npm run build
# Creates optimized build/ folder
```

## 📞 Need Help?

1. **Check browser console** (F12)
2. **Read code comments** - Every function is documented
3. **Check COMPONENTS.md** - Detailed component guide
4. **Check README.md** - Full documentation
5. **Look at examples** - Components have example usage

## 🎯 Common Questions

**Q: Why is the forecast empty?**
A: Click "Train Model" first. The model needs historical data.

**Q: How often does data refresh?**
A: Every 30 seconds automatically.

**Q: Can I use different data sources?**
A: Yes! Edit `src/services/api.js` to connect to different API.

**Q: How do I add more charts?**
A: Create new component in `src/components/`, follow EnergyChart pattern.

**Q: Is this production-ready?**
A: Yes! Follow deployment section to go live.

---

**You're all set! Happy monitoring! 🌱⚡**

For more details, see:
- Full documentation: [README.md](README.md)
- Component guide: [COMPONENTS.md](COMPONENTS.md)
- Backend docs: Check parent directory README
