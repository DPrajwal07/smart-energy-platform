// Energy Card Component
// Displays a metric in a card format (summary statistics)

import React from 'react';
import './EnergyCard.css';

/**
 * EnergyCard Component
 * 
 * Displays a single metric (e.g., total energy, average usage)
 * in an attractive card format with icon and color coding.
 * 
 * Props:
 *   - title: Card title/label
 *   - value: The metric value to display
 *   - unit: Unit of measurement (e.g., "kWh", "tonnes")
 *   - icon: Emoji icon to display
 *   - color: Card color theme (primary, secondary, success, warning)
 */
function EnergyCard({ title, value, unit, icon, color = 'primary' }) {
  return (
    <div className={`energy-card ${color}`}>
      <div className="card-icon">{icon}</div>
      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        <div className="card-value">
          <span className="value">{value}</span>
          <span className="unit">{unit}</span>
        </div>
      </div>
    </div>
  );
}

export default EnergyCard;
