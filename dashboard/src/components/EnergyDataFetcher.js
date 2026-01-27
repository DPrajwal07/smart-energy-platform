// Custom Hook: useEnergyData
// Fetches energy data from FastAPI backend with error and loading handling
// Reusable across multiple components

import { useState, useEffect } from 'react';

/**
 * Custom hook to fetch energy data from FastAPI
 * 
 * Features:
 * - Fetches energy readings from backend
 * - Manages loading state
 * - Handles errors gracefully
 * - Auto-refresh capability
 * - Cleanup on unmount
 * 
 * @param {number} refreshInterval - Milliseconds between auto-refresh (0 = no auto-refresh)
 * @returns {Object} { data, loading, error, refetch }
 * 
 * @example
 * const { data, loading, error, refetch } = useEnergyData(30000);
 * if (loading) return <p>Loading...</p>;
 * if (error) return <p>Error: {error}</p>;
 * return <EnergyChart data={data} />;
 */
export function useEnergyData(refreshInterval = 0) {
  // ========================================================================
  // State Variables
  // ========================================================================
  
  // Energy readings from API
  const [data, setData] = useState([]);
  
  // Loading state (true while fetching)
  const [loading, setLoading] = useState(true);
  
  // Error state (null if no error)
  const [error, setError] = useState(null);

  // ========================================================================
  // Fetch Function
  // ========================================================================
  
  /**
   * Fetch energy data from the backend
   * Handles network errors and invalid responses
   */
  const fetchEnergyData = async () => {
    try {
      // Show loading state
      setLoading(true);
      setError(null);

      // Make API request to backend
      const response = await fetch('http://127.0.0.1:8000/energy/readings');

      // Check if response is OK (status 200-299)
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      // Parse JSON response
      const jsonData = await response.json();

      // Update state with fetched data
      setData(jsonData || []);
      setLoading(false);
    } catch (err) {
      // Handle errors (network, parsing, API errors, etc.)
      console.error('Error fetching energy data:', err);
      setError(err.message || 'Failed to fetch energy data');
      setLoading(false);
      setData([]); // Clear data on error
    }
  };

  // ========================================================================
  // Effect: Fetch on Mount & Auto-Refresh
  // ========================================================================
  
  useEffect(() => {
    // Fetch data immediately when component mounts
    fetchEnergyData();

    // Set up auto-refresh if interval provided
    let interval = null;
    if (refreshInterval > 0) {
      interval = setInterval(fetchEnergyData, refreshInterval);
    }

    // Cleanup: Clear interval and abort pending requests on unmount
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [refreshInterval]);

  // ========================================================================
  // Return Hook Data
  // ========================================================================
  
  return {
    data,      // Energy readings array
    loading,   // Boolean: true if loading
    error,     // String: error message or null
    refetch: fetchEnergyData, // Function to manually refetch
  };
}

/**
 * Component: EnergyDataFetcher
 * 
 * Demonstrates how to use the useEnergyData hook
 * Shows proper handling of loading and error states
 */
function EnergyDataFetcher() {
  // ========================================================================
  // Use the Custom Hook
  // ========================================================================
  
  // Fetch energy data with 30-second auto-refresh
  const { data, loading, error, refetch } = useEnergyData(30000);

  // ========================================================================
  // Render: Loading State
  // ========================================================================
  
  if (loading) {
    return (
      <div className="energy-loader">
        <div className="spinner"></div>
        <p>Loading energy data...</p>
      </div>
    );
  }

  // ========================================================================
  // Render: Error State
  // ========================================================================
  
  if (error) {
    return (
      <div className="energy-error">
        <h3>❌ Error Loading Data</h3>
        <p className="error-message">{error}</p>
        <button onClick={refetch} className="btn-retry">
          Try Again
        </button>
      </div>
    );
  }

  // ========================================================================
  // Render: Success State
  // ========================================================================
  
  return (
    <div className="energy-data-container">
      {/* Header Section */}
      <div className="energy-header">
        <h2>⚡ Energy Data</h2>
        <button onClick={refetch} className="btn-refresh">
          🔄 Refresh
        </button>
      </div>

      {/* Data Display */}
      {data.length > 0 ? (
        <div className="energy-list">
          {/* Summary Stats */}
          <div className="energy-summary">
            <p className="stat">
              <strong>Total Readings:</strong> {data.length}
            </p>
            <p className="stat">
              <strong>Total Energy:</strong>{' '}
              {data
                .reduce((sum, d) => sum + (d.energy_consumed_kwh || 0), 0)
                .toFixed(2)}{' '}
              kWh
            </p>
            <p className="stat">
              <strong>Average:</strong>{' '}
              {data.length > 0
                ? (
                    data.reduce((sum, d) => sum + (d.energy_consumed_kwh || 0), 0) /
                    data.length
                  ).toFixed(2)
                : 0}{' '}
              kWh
            </p>
          </div>

          {/* Data Table */}
          <table className="energy-table">
            <thead>
              <tr>
                <th>Device ID</th>
                <th>Energy (kWh)</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {data.map((reading, index) => (
                <tr key={index}>
                  <td>{reading.device_id || '—'}</td>
                  <td>{reading.energy_consumed_kwh?.toFixed(2) || '—'}</td>
                  <td>
                    {new Date(reading.timestamp).toLocaleString() || '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">
          <p>No energy data available</p>
          <button onClick={refetch} className="btn-retry">
            Fetch Data
          </button>
        </div>
      )}
    </div>
  );
}

export default EnergyDataFetcher;
