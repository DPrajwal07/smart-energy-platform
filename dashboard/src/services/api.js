// API Service for Smart Energy Platform
// Handles all communication with FastAPI backend

import axios from 'axios';

// ============================================================================
// API Configuration
// ============================================================================
// Base URL for the FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// Energy Data Endpoints
// ============================================================================

/**
 * Fetch all energy readings from the database
 * 
 * @returns {Promise} Array of energy readings
 */
export const getEnergyReadings = async () => {
  try {
    const response = await api.get('/energy/readings');
    return response.data;
  } catch (error) {
    console.error('Error fetching energy readings:', error);
    throw error;
  }
};

/**
 * Add a new energy reading
 * 
 * @param {Object} data - Energy reading data
 * @param {string} data.machine_id - Machine identifier
 * @param {number} data.power_kw - Power in kilowatts
 * @param {number} data.energy_consumed_kwh - Energy consumed in kWh
 * 
 * @returns {Promise} Response from server
 */
export const addEnergyReading = async (data) => {
  try {
    const response = await api.post('/energy/add', data);
    return response.data;
  } catch (error) {
    console.error('Error adding energy reading:', error);
    throw error;
  }
};

// ============================================================================
// Prediction Endpoints
// ============================================================================

/**
 * Train the energy prediction model
 * 
 * This endpoint trains a Linear Regression model on historical data.
 * Must be called before making predictions.
 * 
 * @returns {Promise} Training metrics (R² score, MAE, RMSE)
 */
export const trainPredictionModel = async () => {
  try {
    const response = await api.post('/prediction/train');
    return response.data;
  } catch (error) {
    console.error('Error training prediction model:', error);
    throw error;
  }
};

/**
 * Get 7-day energy consumption forecast
 * 
 * Returns hourly predictions organized by day with summaries.
 * Model must be trained first.
 * 
 * @returns {Promise} 7-day forecast with daily summaries
 */
export const getForecast = async () => {
  try {
    const response = await api.get('/prediction/next-7-days');
    return response.data;
  } catch (error) {
    console.error('Error fetching forecast:', error);
    throw error;
  }
};

/**
 * Get prediction model status
 * 
 * Checks if the model is trained and ready for predictions.
 * 
 * @returns {Promise} Model status information
 */
export const getPredictionStatus = async () => {
  try {
    const response = await api.get('/prediction/status');
    return response.data;
  } catch (error) {
    console.error('Error fetching prediction status:', error);
    throw error;
  }
};

// ============================================================================
// Carbon Emissions Endpoints
// ============================================================================

/**
 * Get carbon emissions analysis
 * 
 * Calculates CO2 emissions from energy consumption data.
 * 
 * @param {string|null} machine_id - Optional machine ID to filter by
 * 
 * @returns {Promise} Carbon emissions data with breakdowns
 */
export const getCarbonAnalysis = async (machine_id = null) => {
  try {
    const params = machine_id ? { machine_id } : {};
    const response = await api.get('/sustainability/carbon', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching carbon analysis:', error);
    throw error;
  }
};

// ============================================================================
// Analysis Endpoints
// ============================================================================

/**
 * Get daily energy consumption summary
 * 
 * Calculates daily totals and averages from energy readings.
 * 
 * @returns {Promise} Daily consumption summary
 */
export const getDailyConsumption = async () => {
  try {
    const response = await api.get('/analytics/daily-consumption');
    return response.data;
  } catch (error) {
    console.error('Error fetching daily consumption:', error);
    throw error;
  }
};

// ============================================================================
// Health Check Endpoint
// ============================================================================

/**
 * Check if API is running and responsive
 * 
 * @returns {Promise} Health status
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

export default api;
