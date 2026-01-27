// Status Card Component
// Displays system status information (model status, data points, etc.)

import React from 'react';
import './StatusCard.css';

/**
 * StatusCard Component
 * 
 * Displays a status item with title, value/status, and details.
 * Used to show model training status, data availability, etc.
 * 
 * Props:
 *   - title: Status item title
 *   - status: Main status value or text
 *   - details: Additional description text
 *   - icon: Emoji or icon to display
 */
function StatusCard({ title, status, details, icon }) {
  return (
    <div className="status-card">
      <div className="status-icon">{icon}</div>
      <div className="status-content">
        <h4 className="status-title">{title}</h4>
        <p className="status-value">{status}</p>
        <p className="status-details">{details}</p>
      </div>
    </div>
  );
}

export default StatusCard;
