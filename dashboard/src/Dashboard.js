// Main Dashboard Component
// Orchestrates all dashboard sections and data fetching

import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import EnergyChart from './components/EnergyChart';
import ForecastChart from './components/ForecastChart';
import EnergyCard from './components/EnergyCard';
import StatusCard from './components/StatusCard';
import {
  getEnergyReadings,
  getForecast,
  getPredictionStatus,
  getCarbonAnalysis,
  trainPredictionModel,
} from './services/api';

/**
 * Dashboard Component
 * 
 * Main dashboard that:
 * - Fetches energy data from backend
 * - Displays current energy metrics
 * - Shows historical energy usage chart
 * - Shows 7-day forecast
 * - Shows carbon emissions
 * - Manages model training
 */
function Dashboard() {
  // ========================================================================
  // State Variables
  // ========================================================================
  
  // Energy readings data
  const [energyReadings, setEnergyReadings] = useState([]);
  
  // Forecast data (7-day predictions)
  const [forecast, setForecast] = useState(null);
  
  // Prediction model status
  const [modelStatus, setModelStatus] = useState(null);
  
  // Carbon emissions data
  const [carbonData, setCarbonData] = useState(null);
  
  // Loading and error states
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [trainLoading, setTrainLoading] = useState(false);

  // ========================================================================
  // Fetch Data on Component Mount
  // ========================================================================
  
  useEffect(() => {
    // Function to fetch all dashboard data
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch energy readings
        const readings = await getEnergyReadings();
        setEnergyReadings(readings || []);

        // Fetch prediction status
        const status = await getPredictionStatus();
        setModelStatus(status);

        // Fetch forecast if model is trained
        if (status?.is_trained) {
          try {
            const forecastData = await getForecast();
            setForecast(forecastData);
          } catch (e) {
            console.log('Forecast not available yet');
          }
        }

        // Fetch carbon analysis
        try {
          const carbon = await getCarbonAnalysis();
          setCarbonData(carbon);
        } catch (e) {
          console.log('Carbon data not available');
        }

        setLoading(false);
      } catch (err) {
        setError('Failed to fetch dashboard data. Make sure the API is running.');
        setLoading(false);
      }
    };

    // Call fetch function
    fetchDashboardData();

    // Set up auto-refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);

    // Clean up interval on unmount
    return () => clearInterval(interval);
  }, []);

  // ========================================================================
  // Handler: Train Model
  // ========================================================================
  
  const handleTrainModel = async () => {
    try {
      setTrainLoading(true);
      await trainPredictionModel();
      
      // Refresh status and forecast after training
      const status = await getPredictionStatus();
      setModelStatus(status);

      if (status?.is_trained) {
        const forecastData = await getForecast();
        setForecast(forecastData);
      }

      setTrainLoading(false);
    } catch (err) {
      setError('Failed to train model');
      setTrainLoading(false);
    }
  };

  // ========================================================================
  // Calculate Summary Statistics
  // ========================================================================
  
  // Total energy consumption
  const totalEnergy = energyReadings.reduce(
    (sum, reading) => sum + (reading.energy_consumed_kwh || 0),
    0
  );

  // Average consumption
  const averageEnergy = energyReadings.length > 0
    ? (totalEnergy / energyReadings.length).toFixed(2)
    : 0;

  // Latest reading
  const latestReading = energyReadings[energyReadings.length - 1];

  // ========================================================================
  // Render Dashboard
  // ========================================================================

  return (
    <div className="dashboard">
      {/* ====================================================================
          Header Section
          ==================================================================== */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>⚡ Smart Energy Platform</h1>
          <p className="subtitle">Monitor and optimize your energy usage</p>
        </div>
        <div className="header-actions">
          <button
            className={`btn btn-primary ${trainLoading ? 'loading' : ''}`}
            onClick={handleTrainModel}
            disabled={trainLoading}
          >
            {trainLoading ? '⏳ Training...' : '🤖 Train Model'}
          </button>
          <span className={`status-indicator ${modelStatus?.is_trained ? 'active' : 'inactive'}`}>
            {modelStatus?.is_trained ? '✓ Model Ready' : '○ Model Not Ready'}
          </span>
        </div>
      </header>

      {/* ====================================================================
          Error Alert
          ==================================================================== */}
      {error && (
        <div className="error-alert">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
        </div>
      )}

      {/* ====================================================================
          Loading State
          ==================================================================== */}
      {loading && (
        <div className="loading-container">
          <div className="loader"></div>
          <p>Loading dashboard data...</p>
        </div>
      )}

      {/* ====================================================================
          Main Content
          ==================================================================== */}
      {!loading && (
        <>
          {/* Summary Cards */}
          <section className="summary-cards">
            <EnergyCard
              title="Total Energy"
              value={totalEnergy.toFixed(2)}
              unit="kWh"
              icon="⚡"
              color="primary"
            />
            <EnergyCard
              title="Average Usage"
              value={averageEnergy}
              unit="kWh"
              icon="📊"
              color="secondary"
            />
            <EnergyCard
              title="Latest Reading"
              value={latestReading?.energy_consumed_kwh.toFixed(2) || '—'}
              unit="kWh"
              icon="📈"
              color="success"
            />
            {carbonData && (
              <EnergyCard
                title="Carbon Emissions"
                value={carbonData.emissions?.total_tonnes_co2?.toFixed(2) || '—'}
                unit="tonnes"
                icon="🌍"
                color="warning"
              />
            )}
          </section>

          {/* Charts Section */}
          <section className="charts-section">
            {/* Historical Energy Chart */}
            <div className="chart-container">
              <h2>📈 Energy Usage History</h2>
              {energyReadings.length > 0 ? (
                <EnergyChart data={energyReadings} />
              ) : (
                <div className="empty-state">
                  <p>No energy data available yet</p>
                </div>
              )}
            </div>

            {/* Forecast Chart */}
            <div className="chart-container">
              <h2>🔮 7-Day Forecast</h2>
              {modelStatus?.is_trained && forecast ? (
                <ForecastChart data={forecast} />
              ) : (
                <div className="empty-state">
                  <p>Train the model to see forecast</p>
                  <button
                    className="btn btn-secondary"
                    onClick={handleTrainModel}
                    disabled={trainLoading}
                  >
                    {trainLoading ? 'Training...' : 'Train Now'}
                  </button>
                </div>
              )}
            </div>
          </section>

          {/* Status Cards */}
          {modelStatus && (
            <section className="status-section">
              <h2>📋 System Status</h2>
              <div className="status-cards">
                <StatusCard
                  title="Prediction Model"
                  status={modelStatus?.is_trained ? 'Ready' : 'Not Trained'}
                  details={`Features: ${modelStatus?.features || '—'}`}
                  icon={modelStatus?.is_trained ? '✓' : '○'}
                />
                <StatusCard
                  title="Data Points"
                  status={energyReadings.length}
                  details="Energy readings in database"
                  icon="📚"
                />
                {forecast && (
                  <StatusCard
                    title="Forecast Summary"
                    status={`${forecast.summary?.total_kwh?.toFixed(0)} kWh`}
                    details="Total predicted for 7 days"
                    icon="⚡"
                  />
                )}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}

export default Dashboard;
