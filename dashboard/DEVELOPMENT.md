# Development Tips & Best Practices

Tips for working with the Smart Energy Dashboard codebase.

## 🛠️ Development Workflow

### Daily Workflow

1. **Start backend** (if not running):
   ```bash
   cd ..
   python main.py
   ```

2. **Start dashboard** (in separate terminal):
   ```bash
   cd dashboard
   npm start
   ```

3. **Open browser DevTools:**
   - Windows/Linux: `F12`
   - Mac: `Cmd+Option+I`

4. **Make changes** → Auto-reload in browser (no manual refresh needed)

### Debugging Tips

**View console logs:**
```javascript
console.log('Debug message:', variable);
console.error('Error occurred:', error);
console.warn('Warning:', data);
```

**Check API responses:**
```javascript
const response = await getEnergyReadings();
console.log('API Response:', response);
```

**Monitor state changes:**
```javascript
useEffect(() => {
  console.log('State updated:', energyReadings);
}, [energyReadings]);
```

**Network tab inspection:**
1. Open DevTools (F12)
2. Go to "Network" tab
3. Make an API call
4. Click the request to see details

## 📝 Code Style Guide

### Commenting Best Practices

**Good comment:**
```javascript
// Calculate average energy consumption by dividing total by count
const averageEnergy = totalEnergy / energyReadings.length;
```

**Bad comment:**
```javascript
// Set average
const avg = total / count;
```

### Function Documentation

**Use JSDoc format:**
```javascript
/**
 * Fetches energy readings from backend
 * 
 * @returns {Promise<Array>} Array of energy reading objects
 * @throws {Error} If API call fails
 */
async function getEnergyReadings() {
  // ...
}
```

### Variable Naming

| ❌ Bad | ✅ Good | Why |
|--------|---------|-----|
| `d` | `data` | Clear and descriptive |
| `e` | `error` | Easy to understand |
| `x` | `energyReadings` | Self-documenting |
| `temp` | `formattedData` | Explains purpose |

## 🎨 Styling Best Practices

### Color Consistency

Use the defined color scheme in `src/index.css`:

```css
/* Primary colors */
#667eea - Primary purple
#764ba2 - Secondary purple
#4CAF50 - Success green
#FFC107 - Warning yellow
```

### Responsive Design Pattern

```css
/* Desktop first */
.element {
  width: 100%;
  padding: 20px;
}

/* Tablet */
@media (max-width: 768px) {
  .element {
    padding: 15px;
  }
}

/* Mobile */
@media (max-width: 480px) {
  .element {
    padding: 10px;
  }
}
```

### Class Naming

Use descriptive, hyphenated class names:

```javascript
// Good
<div className="energy-card primary">

// Avoid
<div className="card" style={{...}}>
```

## 🔌 API Integration Patterns

### Adding New API Call

1. **Add function to `src/services/api.js`:**
```javascript
export const getNewData = async () => {
  try {
    const response = await api.get('/new-endpoint');
    return response.data;
  } catch (error) {
    console.error('Error fetching new data:', error);
    throw error;
  }
};
```

2. **Import in Dashboard.js:**
```javascript
import { getNewData } from './services/api';
```

3. **Use with state:**
```javascript
const [newData, setNewData] = useState(null);

useEffect(() => {
  const fetchData = async () => {
    try {
      const data = await getNewData();
      setNewData(data);
    } catch (err) {
      setError('Failed to fetch data');
    }
  };
  fetchData();
}, []);
```

### Error Handling Pattern

```javascript
try {
  const data = await apiCall();
  setData(data);
  setError(null);  // Clear previous errors
} catch (error) {
  console.error('Detailed error for debugging:', error);
  setError('User-friendly error message');
}
```

## ⚡ Performance Optimization

### Prevent Unnecessary Re-renders

```javascript
// Bad: Component re-renders every time (no dependency array)
useEffect(() => {
  fetchData();
});

// Good: Only runs on mount
useEffect(() => {
  fetchData();
}, []);

// Good: Runs when specific dependency changes
useEffect(() => {
  filterData();
}, [filter]);
```

### Optimize List Rendering

```javascript
// Good: Add key prop for list items
{energyReadings.map((reading) => (
  <div key={reading.id}>{reading.energy_consumed_kwh}</div>
))}

// Bad: Don't use index as key
{energyReadings.map((reading, index) => (
  <div key={index}>{reading.energy_consumed_kwh}</div>
))}
```

### Lazy Loading

```javascript
// For future large lists, use React.memo
const EnergyCard = React.memo(({ title, value, unit, icon, color }) => {
  return (
    // Component JSX
  );
});
```

## 🧪 Testing Locally

### Test Different Screen Sizes

```
DevTools → Toggle device toolbar (Ctrl+Shift+M)

Common sizes:
- 1920x1080 (Desktop)
- 768x1024 (Tablet)
- 375x667 (Mobile)
```

### Test API Failures

Simulate API down scenario:
```javascript
// In api.js temporarily:
export const getEnergyReadings = async () => {
  throw new Error('API is down');
};
```

This helps test error UI without stopping the backend.

### Test Slow Network

1. DevTools → Network tab
2. Click throttling dropdown (top)
3. Select "Slow 3G" or "Fast 3G"
4. Make API calls and watch loading behavior

## 📊 Adding Analytics

Track user interactions (optional):

```javascript
// Example: Track model training
const handleTrainModel = async () => {
  console.log('User clicked: Train Model');
  // Track in analytics service
  
  setTrainLoading(true);
  // ... rest of function
};
```

## 🔒 Security Best Practices

### API Keys (if needed)

Don't commit sensitive data:
```javascript
// ❌ BAD - Never do this
const API_KEY = 'sk_live_abc123def456';

// ✅ GOOD - Use environment variables
const API_KEY = process.env.REACT_APP_API_KEY;
```

Create `.env` file:
```
REACT_APP_API_KEY=your_key_here
REACT_APP_API_URL=http://127.0.0.1:8000
```

Access in code:
```javascript
const apiUrl = process.env.REACT_APP_API_URL;
const apiKey = process.env.REACT_APP_API_KEY;
```

## 📦 Dependency Management

### Check what's installed

```bash
npm list
```

### Update dependencies

```bash
npm update  # Updates to latest compatible version

npm outdated  # Shows what can be updated
```

### Add new package

```bash
npm install package-name

# Development only:
npm install --save-dev package-name
```

### Manage versions in package.json

```json
{
  "dependencies": {
    "react": "18.2.0",           // Exact version
    "axios": "^1.6.2",           // Patch updates allowed
    "recharts": "~2.10.3"        // Minor updates allowed
  }
}
```

## 🐛 Common Debugging Scenarios

### Scenario 1: Chart not showing data

```javascript
// Add console logs to debug
const chartData = data.map((reading) => {
  console.log('Raw reading:', reading);
  const formatted = {
    name: new Date(reading.timestamp).toLocaleDateString(),
    consumption: reading.energy_consumed_kwh,
  };
  console.log('Formatted for chart:', formatted);
  return formatted;
});
```

### Scenario 2: API call failing silently

```javascript
const handleTrainModel = async () => {
  try {
    console.log('Starting training...');
    await trainPredictionModel();
    console.log('Training completed successfully');
    // ... update state
  } catch (err) {
    console.error('Training failed:', err.response?.data || err.message);
    setError(err.message);
  }
};
```

### Scenario 3: State not updating

```javascript
// Check if setState is being called
const [energyReadings, setEnergyReadings] = useState([]);

// When updating:
console.log('Before:', energyReadings);
setEnergyReadings(newData);
console.log('After:', energyReadings);  // Still shows old value! (batched update)

// Verify update happened:
useEffect(() => {
  console.log('State updated:', energyReadings);
}, [energyReadings]);
```

## 📱 Responsive Design Checklist

- [ ] Works on mobile (375px width)
- [ ] Works on tablet (768px width)  
- [ ] Works on desktop (1920px width)
- [ ] Text is readable on all sizes
- [ ] Buttons are clickable on mobile
- [ ] Charts don't overflow container
- [ ] Images scale properly
- [ ] No horizontal scroll needed

## 🚀 Before Deploying

### Checklist

- [ ] Remove all `console.log` statements
- [ ] Remove test data
- [ ] Update API URL to production (if different)
- [ ] Test on actual mobile device
- [ ] Check all links work
- [ ] No 404 errors in console
- [ ] Performance is acceptable
- [ ] Security review: no API keys in code
- [ ] Update version number if applicable

### Test Build Locally

```bash
npm run build
npm install -g serve
serve -s build
# Visit http://localhost:3000
```

## 📚 File Organization Tips

### When to create new files

Create new file when:
- Component has >200 lines
- Logic is reusable in multiple places
- File has multiple responsibilities

Keep in same file when:
- Component is <100 lines
- Tightly coupled logic
- Only used in one place

### Import organization

```javascript
// React and third-party imports (top)
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Local imports (below)
import Dashboard from './Dashboard';
import { getEnergyReadings } from './services/api';

// Styles (last)
import './App.css';
```

## 🔄 Git Workflow

```bash
# See changes
git status

# Stage changes
git add .

# Commit with message
git commit -m "feat: Add new chart component"

# Push to GitHub
git push
```

### Commit message conventions

```
feat: Add new feature
fix: Fix a bug
style: Format code
docs: Update documentation
refactor: Reorganize code
test: Add tests
chore: Maintenance
```

## 🎓 Learning Progression

### Week 1
- [ ] Understand component structure
- [ ] Read JSDoc comments
- [ ] Make a small CSS change
- [ ] Trace through one API call

### Week 2
- [ ] Modify a component's JSX
- [ ] Add a new state variable
- [ ] Create a new card component
- [ ] Add console logging for debugging

### Week 3
- [ ] Create a new chart component
- [ ] Add new API function
- [ ] Modify styling significantly
- [ ] Deploy a change

### Week 4+
- [ ] Create complex features
- [ ] Optimize performance
- [ ] Refactor code
- [ ] Mentor others

---

**Happy coding! 💻✨**

For more help, check:
- [React Documentation](https://react.dev)
- [Recharts Documentation](https://recharts.org)
- Component guide: [COMPONENTS.md](COMPONENTS.md)
