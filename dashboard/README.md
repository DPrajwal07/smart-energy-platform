# Smart Energy Platform - React Dashboard

A modern, responsive React dashboard for monitoring and optimizing energy consumption. Features real-time energy data visualization, 7-day forecasts, and carbon emissions tracking.

## 📋 Features

- **⚡ Real-time Energy Monitoring**: Display current and historical energy consumption
- **📈 Interactive Charts**: Visualize energy usage patterns with Recharts
- **🔮 AI-Powered Forecasting**: 7-day energy consumption predictions using Linear Regression
- **🌍 Carbon Tracking**: Monitor CO2 emissions from energy usage
- **🤖 Model Training**: Train machine learning models on historical data
- **📊 Summary Statistics**: Total, average, and latest energy metrics
- **🎨 Professional UI**: Clean, intuitive interface with responsive design
- **💡 Beginner-Friendly Code**: Well-commented, easy-to-understand React components

## 🚀 Quick Start

### Prerequisites

Before you start, make sure you have:
- **Node.js** (v14 or higher) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **FastAPI Backend Running** on `http://127.0.0.1:8000`

### Installation

1. **Navigate to dashboard folder:**
   ```bash
   cd dashboard
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

The dashboard will automatically open in your browser at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## 📁 Project Structure

```
dashboard/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/             # React components
│   │   ├── EnergyChart.js       # Historical energy chart
│   │   ├── ForecastChart.js     # 7-day forecast chart
│   │   ├── EnergyCard.js        # Summary metric card
│   │   ├── StatusCard.js        # Status display card
│   │   ├── EnergyCard.css
│   │   └── StatusCard.css
│   ├── services/
│   │   └── api.js              # API integration (8 endpoints)
│   ├── App.js                  # Main app component
│   ├── App.css
│   ├── Dashboard.js            # Dashboard container
│   ├── Dashboard.css
│   ├── index.js                # React entry point
│   └── index.css               # Global styles
├── package.json                # Dependencies
└── README.md                   # This file
```

## 🔌 API Integration

The dashboard connects to your FastAPI backend using 8 endpoints. All API calls are centralized in `src/services/api.js`:

### Available API Functions

| Function | Purpose | Status |
|----------|---------|--------|
| `getEnergyReadings()` | Fetch all energy readings | ✅ Ready |
| `addEnergyReading(data)` | Add new energy reading | ✅ Ready |
| `trainPredictionModel()` | Train ML model | ✅ Ready |
| `getForecast()` | Get 7-day predictions | ✅ Ready |
| `getPredictionStatus()` | Check model status | ✅ Ready |
| `getCarbonAnalysis()` | Get CO2 emissions | ✅ Ready |
| `getDailyConsumption()` | Daily summary stats | ✅ Ready |
| `healthCheck()` | API health status | ✅ Ready |

### Backend Requirements

The FastAPI backend should provide these endpoints:

- `GET /energy/readings` - Returns array of energy readings
- `POST /energy/add` - Creates new energy reading
- `POST /prediction/train` - Trains prediction model
- `GET /prediction/next-7-days` - Returns 7-day forecast
- `GET /prediction/status` - Returns model training status
- `GET /sustainability/carbon` - Returns carbon emissions data
- `GET /analytics/daily-consumption` - Returns daily summary
- `GET /health` - Returns API health status

## 🧩 Component Architecture

### Dashboard Component
The main container that orchestrates all other components:
- Fetches data from API
- Manages loading and error states
- Displays summary cards and charts
- Handles model training

**Features:**
- Automatic data refresh every 30 seconds
- Comprehensive error handling
- Loading spinner while fetching
- Train model button with status updates

### Chart Components

#### EnergyChart
Displays historical energy consumption as a line chart using Recharts.
- Shows all available energy readings
- Date-based X-axis
- Energy consumption in kWh on Y-axis
- Interactive tooltips on hover

#### ForecastChart
Shows 7-day energy consumption predictions as a bar chart.
- Displays daily average predictions
- Green colored bars for forecasts
- Helpful for planning energy usage

### Card Components

#### EnergyCard
Displays individual metrics in an attractive card format.
- Configurable title, value, unit, icon, and color
- Four color variants: primary, secondary, success, warning
- Hover animation effect

#### StatusCard
Shows system status information.
- Model training status
- Data availability metrics
- Forecast summary

## 💻 Component Usage Examples

### Using the API in Components

```javascript
import { getForecast, getEnergyReadings } from './services/api';

// In useEffect or event handler:
const fetchData = async () => {
  try {
    const forecast = await getForecast();
    setForecast(forecast);
  } catch (error) {
    console.error('Failed to fetch forecast');
  }
};
```

### Creating Custom Cards

```javascript
<EnergyCard
  title="Total Energy"
  value={1234.56}
  unit="kWh"
  icon="⚡"
  color="primary"
/>
```

## 🎨 Styling & Customization

### Global Colors

Edit `src/index.css` to customize the color scheme:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Accent colors */
--primary: #667eea;
--success: #4CAF50;
--warning: #FFC107;
```

### Responsive Design

The dashboard is fully responsive and works on:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

Media queries adjust layout and font sizes for smaller screens.

## 🔧 Troubleshooting

### Dashboard shows "API Connection Error"

**Solution:** Make sure your FastAPI backend is running:
```bash
# In another terminal, go to your backend folder
python main.py
```

Backend should be running on `http://127.0.0.1:8000`

### No data showing in charts

**Possible causes:**
1. Backend API is not returning data
2. Energy readings not yet added to database
3. Prediction model not trained yet

**Solutions:**
- Check backend API responses using Postman or curl
- Add sample energy readings through the API
- Click "Train Model" button to train predictions

### Port 3000 already in use

```bash
# Use a different port
PORT=3001 npm start
```

### Charts not displaying correctly

- Make sure Recharts is installed: `npm install recharts`
- Check browser console for JavaScript errors
- Try clearing browser cache and hard refresh

## 📚 Learning Resources

### For Beginners

1. **React Basics**
   - Components and props
   - State and hooks (useState, useEffect)
   - Event handling

2. **Key Concepts Used**
   - **useState**: Managing component state (data, loading, error)
   - **useEffect**: Fetching data when component mounts
   - **async/await**: Handling API calls
   - **Array methods**: map(), reduce() for data transformation

3. **Code Comments**
   - Every component and function is well-commented
   - Look for `// ====` section dividers for major sections
   - JSDoc comments explain what each function does

### Resources for Learning More

- [React Documentation](https://react.dev)
- [Recharts Documentation](https://recharts.org)
- [Axios Documentation](https://axios-http.com)
- [JavaScript Async/Await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous)

## 📝 Adding New Features

### Example: Add a new chart

1. Create new file: `src/components/NewChart.js`
2. Import Recharts components
3. Import data-fetching function from `services/api.js`
4. Add component to Dashboard.js
5. Style with CSS

### Example: Add a new API endpoint

1. Add function to `src/services/api.js`
2. Include JSDoc comments
3. Use in components with try-catch
4. Handle loading and error states

## 🚀 Deployment

### Deploy to Vercel (Recommended)

1. Push code to GitHub
2. Connect GitHub to [Vercel](https://vercel.com)
3. Vercel automatically builds and deploys

### Deploy to Netlify

1. Run `npm run build`
2. Drag-and-drop `build/` folder to Netlify
3. Update API URL if backend is on different server

### Deploy to Custom Server

```bash
npm run build
# Copy build/ folder to your server
# Configure web server (nginx/apache) to serve static files
```

## 📞 Support & Contributing

### Getting Help

- Check the comments in the code
- Review the component structure
- Check browser console for errors
- Verify backend API is running

### Contributing

To improve the dashboard:
1. Make changes to components
2. Test locally with `npm start`
3. Check for errors in console
4. Document your changes

## 📄 License

This project is part of the Smart Energy Platform system.

## 🎯 Next Steps

1. ✅ Start the development server: `npm start`
2. ✅ Train the prediction model (click "Train Model" button)
3. ✅ Explore the charts and metrics
4. ✅ Customize colors and styling to your preference
5. ✅ Deploy to production when ready

---

**Happy monitoring! 🌱⚡**

For issues or questions about the FastAPI backend, see the backend documentation.
