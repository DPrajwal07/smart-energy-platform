# 📚 React Fetch Component Guide

Complete guide to using the `EnergyDataFetcher` component with proper error and loading state handling.

## 📋 Overview

The component demonstrates best practices for:
- ✅ Fetching data with the Fetch API
- ✅ Managing loading state
- ✅ Handling errors gracefully
- ✅ Auto-refresh capability
- ✅ Reusable custom hook pattern
- ✅ Clean, readable code

---

## 🎯 Component Architecture

### Two-Part Design

```
useEnergyData (Custom Hook)
    ↓
    Handles: fetching, state management, auto-refresh
    ↓
    Returns: { data, loading, error, refetch }
    ↓
EnergyDataFetcher (Component)
    ↓
    Handles: UI rendering, user interaction
    ↓
    Uses hook to manage data
```

---

## 🚀 Basic Usage

### Simple Implementation

```javascript
import EnergyDataFetcher from './components/EnergyDataFetcher';

function App() {
  return (
    <div>
      <h1>Energy Dashboard</h1>
      <EnergyDataFetcher />
    </div>
  );
}

export default App;
```

### Using the Hook Directly

```javascript
import { useEnergyData } from './components/EnergyDataFetcher';

function MyCustomComponent() {
  // Fetch data with 30-second auto-refresh
  const { data, loading, error, refetch } = useEnergyData(30000);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Energy Readings: {data.length}</h2>
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}

export default MyCustomComponent;
```

---

## 🔍 Detailed Explanation

### The useEnergyData Hook

#### Hook Structure
```javascript
const { data, loading, error, refetch } = useEnergyData(refreshInterval);
```

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `refreshInterval` | number (ms) | 0 | Auto-refresh interval (0 = disabled) |

#### Return Values
| Value | Type | Description |
|-------|------|-------------|
| `data` | Array | Energy readings from API |
| `loading` | Boolean | True while fetching |
| `error` | String \| null | Error message or null |
| `refetch` | Function | Manually refetch data |

### State Management

#### 1. Loading State
```javascript
const [loading, setLoading] = useState(true);
```
- `true` = data is being fetched
- `false` = data fetch complete (success or error)

#### 2. Error State
```javascript
const [error, setError] = useState(null);
```
- `null` = no error
- `string` = error message from API or network

#### 3. Data State
```javascript
const [data, setData] = useState([]);
```
- Empty array `[]` initially
- Populated with API response when successful
- Cleared on error

### Fetch Function Breakdown

```javascript
const fetchEnergyData = async () => {
  try {
    // 1. Set loading = true
    setLoading(true);
    setError(null);

    // 2. Make API request
    const response = await fetch('http://127.0.0.1:8000/energy/readings');

    // 3. Check response status
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    // 4. Parse JSON
    const jsonData = await response.json();

    // 5. Update state (success)
    setData(jsonData || []);
    setLoading(false);

  } catch (err) {
    // 6. Handle errors
    console.error('Error:', err);
    setError(err.message);
    setLoading(false);
    setData([]); // Clear data on error
  }
};
```

### Auto-Refresh Logic

```javascript
useEffect(() => {
  // 1. Fetch immediately on mount
  fetchEnergyData();

  // 2. Set up auto-refresh if interval provided
  let interval = null;
  if (refreshInterval > 0) {
    interval = setInterval(fetchEnergyData, refreshInterval);
  }

  // 3. Cleanup on unmount
  return () => {
    if (interval) {
      clearInterval(interval);
    }
  };
}, [refreshInterval]);
```

---

## 🎨 UI States

### Loading State
```javascript
if (loading) {
  return (
    <div className="energy-loader">
      <div className="spinner"></div>
      <p>Loading energy data...</p>
    </div>
  );
}
```
Shows: Animated spinner + message

### Error State
```javascript
if (error) {
  return (
    <div className="energy-error">
      <h3>❌ Error Loading Data</h3>
      <p className="error-message">{error}</p>
      <button onClick={refetch}>Try Again</button>
    </div>
  );
}
```
Shows: Error message + retry button

### Success State
```javascript
return (
  <div className="energy-data-container">
    <div className="energy-header">
      <h2>⚡ Energy Data</h2>
      <button onClick={refetch}>🔄 Refresh</button>
    </div>
    
    <div className="energy-summary">
      {/* Summary stats */}
    </div>
    
    <table className="energy-table">
      {/* Data table */}
    </table>
  </div>
);
```
Shows: Data table + summary stats + refresh button

---

## 📊 Common Patterns

### Pattern 1: Auto-Refresh Every 30 Seconds
```javascript
const { data, loading, error } = useEnergyData(30000);
```

### Pattern 2: No Auto-Refresh
```javascript
const { data, loading, error, refetch } = useEnergyData(0);

// Fetch on button click
<button onClick={refetch}>Load Data</button>
```

### Pattern 3: Fetch Every Minute
```javascript
const { data, loading, error } = useEnergyData(60000);
```

### Pattern 4: Use in Multiple Components
```javascript
// Component 1: Shows as table
function DataTable() {
  const { data, loading } = useEnergyData(30000);
  if (loading) return <LoadingSpinner />;
  return <Table data={data} />;
}

// Component 2: Shows as chart
function EnergyChart() {
  const { data, loading } = useEnergyData(30000);
  if (loading) return <LoadingSpinner />;
  return <Chart data={data} />;
}

// Both share the same data source!
```

---

## 🔧 Customization

### Change API URL
```javascript
// In fetchEnergyData function:
const response = await fetch('YOUR_API_URL/energy/readings');
```

### Custom Error Messages
```javascript
if (!response.ok) {
  // Instead of generic error:
  // throw new Error(`API Error: ${response.status}`);
  
  // Use custom message:
  const errorText = await response.text();
  throw new Error(`Failed to load energy data: ${errorText}`);
}
```

### Add Request Headers
```javascript
const response = await fetch('http://127.0.0.1:8000/energy/readings', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN', // If needed
  },
});
```

### Add Request Timeout
```javascript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 sec timeout

try {
  const response = await fetch(url, {
    signal: controller.signal,
  });
  clearTimeout(timeoutId);
  // ... rest of code
} catch (err) {
  if (err.name === 'AbortError') {
    setError('Request timeout - please try again');
  }
}
```

---

## 🐛 Error Handling

### Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to fetch` | Network error / CORS issue | Check backend running |
| `API Error: 404` | Wrong endpoint | Verify API URL |
| `JSON.parse error` | Invalid JSON response | Check API returns JSON |
| `TypeError` | Network completely down | Check internet connection |

### Debug Tips

```javascript
// Add console logs to see what's happening
const fetchEnergyData = async () => {
  try {
    console.log('Starting fetch...');
    const response = await fetch(url);
    console.log('Response status:', response.status);
    
    const jsonData = await response.json();
    console.log('Parsed data:', jsonData);
    
    setData(jsonData || []);
  } catch (err) {
    console.error('Full error object:', err);
    console.error('Error message:', err.message);
  }
};
```

---

## 📱 Responsive Design

The component is fully responsive:

| Screen Size | Layout | Behavior |
|-------------|--------|----------|
| Desktop (1200px+) | Table with 3 columns | Full table visible |
| Tablet (768-1199px) | Responsive grid | Table adjusts |
| Mobile (<768px) | Stacked cards | Table becomes card list |

---

## ♿ Accessibility

The component includes:
- ✅ Semantic HTML (table, button)
- ✅ Clear error messages
- ✅ Loading indicator
- ✅ Keyboard accessible buttons
- ✅ ARIA-friendly structure

---

## ⚡ Performance

### Optimization Techniques Used

1. **Dependency Array in useEffect**
   - Only refetches when `refreshInterval` changes
   - Prevents unnecessary re-renders

2. **State Cleanup**
   - Clears interval on unmount
   - Prevents memory leaks

3. **Early Returns**
   - Avoids rendering data when loading/error
   - Reduces DOM updates

### Further Optimizations

```javascript
// Use React.memo to prevent re-renders
const EnergyDataFetcher = React.memo(function EnergyDataFetcher() {
  // ... component code
});
```

---

## 🔄 Comparison: Fetch vs Axios

### This Component (Fetch API)
```javascript
const response = await fetch(url);
const data = await response.json();
```

**Pros:**
- ✅ Built-in (no extra library)
- ✅ Lightweight
- ✅ Modern standard

**Cons:**
- ❌ Verbose error handling
- ❌ No automatic JSON parsing
- ❌ No request cancellation

### Using Axios (Alternative)
```javascript
const data = await axios.get(url);
```

**Pros:**
- ✅ Simpler syntax
- ✅ Better error handling
- ✅ Request cancellation

**Cons:**
- ❌ Extra dependency
- ❌ Slightly larger bundle

> Both are valid! This component teaches Fetch API fundamentals.

---

## 🎓 Learning Points

### Key Concepts

1. **useEffect with Dependencies**
   - Runs code after render
   - Cleanup function prevents leaks
   - Dependency array controls when to run

2. **Async/Await**
   - Makes async code look synchronous
   - Try-catch for error handling
   - Cleaner than .then() chains

3. **State Management**
   - Loading, error, and data states
   - Update states for different scenarios
   - Proper cleanup on errors

4. **Custom Hooks**
   - Reusable logic across components
   - Share state between components
   - Keep components clean and simple

5. **Error Boundaries**
   - Handle errors gracefully
   - Show helpful messages to users
   - Provide recovery options (retry)

---

## 📚 Related Documentation

- [React Hooks Documentation](https://react.dev/reference/react)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Async/Await Tutorial](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises)
- [Error Handling in React](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)

---

## ✅ Checklist

After using this component, you should understand:
- [ ] How to fetch data with the Fetch API
- [ ] How to use useEffect for side effects
- [ ] How to manage loading and error states
- [ ] How to handle async operations in React
- [ ] How to create reusable custom hooks
- [ ] How to structure error boundaries
- [ ] How to implement auto-refresh
- [ ] How to clean up effects on unmount

---

## 🎯 Next Steps

1. **Use the component:** Import it in your app
2. **Customize it:** Modify to fit your needs
3. **Study it:** Read the code and understand each part
4. **Extend it:** Add filtering, sorting, etc.
5. **Build with it:** Create more complex components

---

**Happy fetching!** 🚀

For questions, check the code comments or refer to the React documentation.
