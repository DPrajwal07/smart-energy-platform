// Forecast Chart Component
// Displays 7-day energy forecast using Recharts bar chart

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

/**
 * ForecastChart Component
 * 
 * Displays predicted energy consumption for the next 7 days
 * in a bar chart format.
 * 
 * Props:
 *   - data: Forecast object containing hourly predictions
 */
function ForecastChart({ data }) {
  // Handle missing data
  if (!data || !data.predictions) {
    return <p>No forecast data available</p>;
  }

  // Prepare data for chart
  // Group predictions by date
  const chartData = {};

  // Process each prediction
  (data.predictions || []).forEach((prediction) => {
    const date = new Date(prediction.timestamp);
    const dateKey = date.toLocaleDateString();

    if (!chartData[dateKey]) {
      chartData[dateKey] = {
        name: dateKey,
        prediction: 0,
        count: 0,
      };
    }

    // Average the hourly predictions by day
    chartData[dateKey].prediction += prediction.predicted_consumption;
    chartData[dateKey].count += 1;
  });

  // Calculate daily averages
  const formattedData = Object.values(chartData).map((day) => ({
    ...day,
    prediction: (day.prediction / day.count).toFixed(2),
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload[0]) {
      return (
        <div className="custom-tooltip">
          <p className="label">Date: {payload[0].payload.name}</p>
          <p className="value">
            Predicted: {payload[0].value} kWh (daily average)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={formattedData}
        margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis
          dataKey="name"
          stroke="#666"
          style={{ fontSize: '12px' }}
        />
        <YAxis
          stroke="#666"
          label={{ value: 'Energy (kWh)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Bar
          dataKey="prediction"
          fill="#4CAF50"
          name="Predicted Energy"
          radius={[8, 8, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default ForecastChart;
