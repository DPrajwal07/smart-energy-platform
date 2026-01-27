// Main App Component
// Root component that renders the dashboard

import React from 'react';
import Dashboard from './Dashboard';
import './App.css';

/**
 * App Component
 * 
 * Root React component. Renders the main dashboard.
 * This is the entry point for the entire application.
 */
function App() {
  return (
    <div className="app">
      <Dashboard />
    </div>
  );
}

export default App;
