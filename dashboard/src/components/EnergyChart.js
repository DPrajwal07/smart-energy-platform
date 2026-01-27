// Energy Chart Component
// Displays historical energy consumption using Recharts

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

/**
 * EnergyChart Component
 * 
 * Displays historical energy consumption data in a line chart.
 * 
 * Props:
 *   - data: Array of energy reading objects with timestamp and energy_consumed_kwh
 */
function EnergyChart({ data }) {
  // Handle empty data
  if (!data || data.length === 0) {
    return <p>No data to display</p>;
  }

  // Transform data for chart: format the timestamps
  const chartData = data.map((reading) => ({
    name: new Date(reading.timestamp).toLocaleDateString(),
    consumption: reading.energy_consumed_kwh,
    timestamp: reading.timestamp,
  }));

  // Custom tooltip to show formatted data
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload[0]) {
      return (
        <div className="custom-tooltip">
          <p className="label">
            Date: {new Date(payload[0].payload.timestamp).toLocaleString()}
          </p>
          <p className="value">
            Consumption: {payload[0].value.toFixed(2)} kWh
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart
        data={chartData}
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
        <Line
          type="monotone"
          dataKey="consumption"
          stroke="#2196F3"
          strokeWidth={2}
          dot={{ fill: '#2196F3', r: 5 }}
          activeDot={{ r: 7 }}
          name="Energy Consumption"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default EnergyChart;
