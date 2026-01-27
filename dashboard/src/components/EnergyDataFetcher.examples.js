// Example Usage Patterns for EnergyDataFetcher Component
// These examples show how to use the component and hook in different scenarios

// ========================================================================
// EXAMPLE 1: Simple Component Usage (Easiest)
// ========================================================================

import EnergyDataFetcher from './components/EnergyDataFetcher';

/**
 * Simply import and use the component
 * No additional setup needed
 */
function Example1_SimpleUsage() {
  return (
    <div>
      <h1>My Energy Dashboard</h1>
      <EnergyDataFetcher />
    </div>
  );
}

// ========================================================================
// EXAMPLE 2: Using the Hook with Custom UI
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';

/**
 * Use the hook directly to build custom UI
 * Full control over the UI while managing data fetching
 */
function Example2_CustomUI() {
  // Fetch energy data with 30-second auto-refresh
  const { data, loading, error, refetch } = useEnergyData(30000);

  return (
    <div style={{ padding: '20px' }}>
      <h1>⚡ Energy Monitor</h1>

      {/* Show loading spinner */}
      {loading && (
        <div>
          <div className="spinner"></div>
          <p>Fetching energy data...</p>
        </div>
      )}

      {/* Show error message */}
      {error && (
        <div style={{ color: 'red', padding: '10px', border: '1px solid red' }}>
          <p>Error: {error}</p>
          <button onClick={refetch}>Retry</button>
        </div>
      )}

      {/* Show data */}
      {!loading && !error && (
        <div>
          <p>Total readings: {data.length}</p>
          <button onClick={refetch}>Refresh Data</button>

          {data.length > 0 ? (
            <ul>
              {data.slice(0, 5).map((reading, idx) => (
                <li key={idx}>
                  {reading.device_id}: {reading.energy_consumed_kwh} kWh
                </li>
              ))}
            </ul>
          ) : (
            <p>No data available</p>
          )}
        </div>
      )}
    </div>
  );
}

// ========================================================================
// EXAMPLE 3: Without Auto-Refresh (Manual Refetch)
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';

/**
 * Use the hook without auto-refresh
 * User controls when data is fetched
 */
function Example3_ManualRefresh() {
  // 0 = no auto-refresh
  const { data, loading, error, refetch } = useEnergyData(0);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Energy Data (Manual Refresh)</h1>

      <button
        onClick={refetch}
        disabled={loading}
        style={{
          padding: '10px 20px',
          background: '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer',
        }}
      >
        {loading ? 'Loading...' : 'Load Data'}
      </button>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {data.length > 0 && (
        <p>Loaded {data.length} readings</p>
      )}
    </div>
  );
}

// ========================================================================
// EXAMPLE 4: With Different Refresh Intervals
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';

/**
 * Use different refresh intervals for different components
 */
function Example4_DifferentIntervals() {
  // Refresh every 10 seconds
  const { data: fastData } = useEnergyData(10000);

  // Refresh every 60 seconds
  const { data: slowData } = useEnergyData(60000);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Energy Monitoring</h1>

      <div>
        <h2>Real-Time (10 sec refresh)</h2>
        <p>Current readings: {fastData.length}</p>
      </div>

      <div>
        <h2>Summary (60 sec refresh)</h2>
        <p>Total readings: {slowData.length}</p>
      </div>
    </div>
  );
}

// ========================================================================
// EXAMPLE 5: Error Boundary with Retry Logic
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';
import { useState } from 'react';

/**
 * Advanced: Handle errors with retry counter
 */
function Example5_RetryLogic() {
  const { data, loading, error, refetch } = useEnergyData(30000);
  const [retryCount, setRetryCount] = useState(0);

  const handleRetry = () => {
    refetch();
    setRetryCount(retryCount + 1);
  };

  return (
    <div style={{ padding: '20px' }}>
      {loading && <p>Loading...</p>}

      {error && (
        <div style={{ background: '#ffebee', padding: '15px' }}>
          <p>Error: {error}</p>
          <p>Retry attempts: {retryCount}</p>
          <button onClick={handleRetry}>
            Try Again
          </button>
        </div>
      )}

      {!loading && !error && <p>Data loaded: {data.length} readings</p>}
    </div>
  );
}

// ========================================================================
// EXAMPLE 6: Multiple Components Sharing Same Data
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';

/**
 * Create a hook factory to share data across components
 */
function SharedDataProvider() {
  // Fetch once here
  const energyData = useEnergyData(30000);

  return (
    <div>
      <h1>Shared Data Example</h1>

      {/* Pass data to child components */}
      <DataTable data={energyData} />
      <DataChart data={energyData} />
      <DataSummary data={energyData} />
    </div>
  );
}

function DataTable({ data: { data, loading, error } }) {
  if (loading) return <p>Loading table...</p>;
  if (error) return <p>Error: {error}</p>;
  return <table>{/* Table content */}</table>;
}

function DataChart({ data: { data, loading } }) {
  if (loading) return <p>Loading chart...</p>;
  return <div>{/* Chart content */}</div>;
}

function DataSummary({ data: { data, loading, refetch } }) {
  if (loading) return <p>Loading summary...</p>;
  return (
    <div>
      <p>Total: {data.length}</p>
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}

// ========================================================================
// EXAMPLE 7: Conditional Auto-Refresh
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';
import { useState } from 'react';

/**
 * Toggle auto-refresh on and off
 */
function Example7_ConditionalRefresh() {
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Refresh only when autoRefresh is true
  const { data, loading, error, refetch } = useEnergyData(
    autoRefresh ? 30000 : 0
  );

  return (
    <div style={{ padding: '20px' }}>
      <h1>Energy Data</h1>

      <label>
        <input
          type="checkbox"
          checked={autoRefresh}
          onChange={(e) => setAutoRefresh(e.target.checked)}
        />
        Auto-refresh every 30 seconds
      </label>

      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {data.length > 0 && <p>Readings: {data.length}</p>}

      {!autoRefresh && (
        <button onClick={refetch}>Refresh Now</button>
      )}
    </div>
  );
}

// ========================================================================
// EXAMPLE 8: With Data Filtering
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';
import { useState } from 'react';

/**
 * Fetch data and filter it based on user input
 */
function Example8_WithFiltering() {
  const { data, loading, error } = useEnergyData(30000);
  const [filter, setFilter] = useState('');

  // Filter data based on device ID
  const filteredData = data.filter((reading) =>
    reading.device_id?.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div style={{ padding: '20px' }}>
      <h1>Energy Data</h1>

      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}

      {!loading && !error && (
        <>
          <input
            type="text"
            placeholder="Filter by device ID..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            style={{
              padding: '10px',
              width: '100%',
              marginBottom: '15px',
              border: '1px solid #ccc',
              borderRadius: '4px',
            }}
          />

          <p>Showing {filteredData.length} of {data.length} readings</p>

          <ul>
            {filteredData.map((reading, idx) => (
              <li key={idx}>
                {reading.device_id}: {reading.energy_consumed_kwh} kWh
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

// ========================================================================
// EXAMPLE 9: Data Transformation
// ========================================================================

import { useEnergyData } from './components/EnergyDataFetcher';
import { useMemo } from 'react';

/**
 * Transform and calculate statistics from fetched data
 */
function Example9_DataTransformation() {
  const { data, loading, error } = useEnergyData(30000);

  // Calculate statistics (only recalculate when data changes)
  const stats = useMemo(() => {
    if (data.length === 0) {
      return { total: 0, average: 0, max: 0, min: 0 };
    }

    const values = data.map((d) => d.energy_consumed_kwh);
    return {
      total: values.reduce((sum, v) => sum + v, 0).toFixed(2),
      average: (
        values.reduce((sum, v) => sum + v, 0) / values.length
      ).toFixed(2),
      max: Math.max(...values).toFixed(2),
      min: Math.min(...values).toFixed(2),
    };
  }, [data]);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Energy Statistics</h1>

      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}

      {!loading && !error && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr' }}>
          <div>
            <h3>Total</h3>
            <p>{stats.total} kWh</p>
          </div>
          <div>
            <h3>Average</h3>
            <p>{stats.average} kWh</p>
          </div>
          <div>
            <h3>Maximum</h3>
            <p>{stats.max} kWh</p>
          </div>
          <div>
            <h3>Minimum</h3>
            <p>{stats.min} kWh</p>
          </div>
        </div>
      )}
    </div>
  );
}

// ========================================================================
// EXAMPLE 10: Export all examples
// ========================================================================

export {
  Example1_SimpleUsage,
  Example2_CustomUI,
  Example3_ManualRefresh,
  Example4_DifferentIntervals,
  Example5_RetryLogic,
  Example6_SharedDataProvider,
  Example7_ConditionalRefresh,
  Example8_WithFiltering,
  Example9_DataTransformation,
};
