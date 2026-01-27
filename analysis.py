# Energy Data Analysis Module for Smart Energy Platform
# This module provides functions to analyze energy consumption patterns
# using Pandas and simple statistical methods

# Import required libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# ============================================================================
# SECTION 1: Daily Energy Consumption Analysis
# ============================================================================

def calculate_daily_consumption(
    df: pd.DataFrame,
    date_column: str = 'timestamp',
    energy_column: str = 'energy_consumed_kwh'
) -> pd.DataFrame:
    """
    Calculate total daily energy consumption from hourly/minute readings.
    
    How it works:
    1. Convert timestamp to date (removing time component)
    2. Group readings by date
    3. Calculate the sum of energy for each day
    
    Args:
        df: DataFrame with timestamp and energy columns
        date_column: Name of timestamp column (default: 'timestamp')
        energy_column: Name of energy consumption column
    
    Returns:
        DataFrame with columns: date, total_energy_kwh
    
    Example:
        >>> df = pd.DataFrame({
        ...     'timestamp': ['2026-01-01 08:00', '2026-01-01 09:00', '2026-01-02 08:00'],
        ...     'energy_consumed_kwh': [100, 150, 200]
        ... })
        >>> daily = calculate_daily_consumption(df)
        >>> print(daily)
                date  total_energy_kwh
        0  2026-01-01             250.0
        1  2026-01-02             200.0
    """
    # ========================================================================
    # Step 1: Make a copy to avoid modifying original data
    # ========================================================================
    data = df.copy()
    
    # ========================================================================
    # Step 2: Convert timestamp column to datetime if it isn't already
    # ========================================================================
    data[date_column] = pd.to_datetime(data[date_column])
    
    # ========================================================================
    # Step 3: Extract just the date part (remove time)
    # ========================================================================
    data['date'] = data[date_column].dt.date
    
    # ========================================================================
    # Step 4: Group by date and sum the energy consumption
    # ========================================================================
    # This calculates total energy used each day
    daily_consumption = data.groupby('date')[energy_column].sum().reset_index()
    
    # ========================================================================
    # Step 5: Rename column for clarity
    # ========================================================================
    daily_consumption.columns = ['date', 'total_energy_kwh']
    
    # ========================================================================
    # Step 6: Return the result
    # ========================================================================
    return daily_consumption


# ============================================================================
# SECTION 2: Peak Load Period Identification
# ============================================================================

def identify_peak_periods(
    df: pd.DataFrame,
    power_column: str = 'power_kw',
    percentile: float = 75.0
) -> Dict:
    """
    Identify peak load periods using percentile analysis.
    
    How it works:
    1. Calculate the Xth percentile of power (default: 75th percentile)
    2. Find all periods where power exceeds this threshold
    3. Return statistics about peak periods
    
    Args:
        df: DataFrame with power consumption column
        power_column: Name of power consumption column (default: 'power_kw')
        percentile: Percentile threshold (0-100, default: 75)
    
    Returns:
        Dictionary with:
        - peak_threshold: Power level considered as peak
        - peak_count: Number of peak period readings
        - peak_percentage: % of time at peak load
        - average_peak_power: Average power during peak periods
    
    Example:
        >>> df = pd.DataFrame({
        ...     'power_kw': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        ... })
        >>> peaks = identify_peak_periods(df, percentile=75)
        >>> print(f"Peak threshold: {peaks['peak_threshold']} kW")
    """
    # ========================================================================
    # Step 1: Calculate the percentile threshold
    # ========================================================================
    # Example: 75th percentile means this is the point where 75% of values
    # are below and 25% are above
    peak_threshold = df[power_column].quantile(percentile / 100)
    
    # ========================================================================
    # Step 2: Find all readings at or above the threshold
    # ========================================================================
    peak_readings = df[df[power_column] >= peak_threshold]
    
    # ========================================================================
    # Step 3: Calculate statistics
    # ========================================================================
    peak_count = len(peak_readings)
    total_count = len(df)
    peak_percentage = (peak_count / total_count) * 100
    average_peak_power = peak_readings[power_column].mean()
    
    # ========================================================================
    # Step 4: Create result dictionary
    # ========================================================================
    result = {
        'peak_threshold': float(peak_threshold),
        'peak_count': int(peak_count),
        'peak_percentage': float(peak_percentage),
        'average_peak_power': float(average_peak_power),
        'min_peak_power': float(peak_readings[power_column].min()),
        'max_peak_power': float(peak_readings[power_column].max())
    }
    
    return result


# ============================================================================
# SECTION 3: Abnormal Spike Detection using Rolling Average
# ============================================================================

def detect_abnormal_spikes(
    df: pd.DataFrame,
    power_column: str = 'power_kw',
    window_size: int = 5,
    deviation_threshold: float = 2.0
) -> pd.DataFrame:
    """
    Detect abnormal power spikes using rolling average method.
    
    How it works:
    1. Calculate rolling (moving) average of power consumption
       - This smooths out normal fluctuations
       - Shows the underlying trend
    2. Calculate deviation: actual power - rolling average
    3. Find spikes where deviation exceeds threshold
    4. Mark these as anomalies
    
    Rolling Average Example:
        Power: [10, 12, 15, 20, 18, 100, 16, 14, 12]
        Rolling avg (window=3): [-, -, 12.33, 15.67, 17.67, 46, 44.67, 43.33, 14]
        Deviation: [-, -, 2.67, 4.33, 0.33, 54, -28.67, -29.33, -2]
        Spike at position 5 (value 100) because deviation = 54 is very high
    
    Args:
        df: DataFrame with power consumption column
        power_column: Name of power column (default: 'power_kw')
        window_size: Number of readings for rolling average (default: 5)
        deviation_threshold: How many std devs above normal to flag as spike
    
    Returns:
        DataFrame with original data plus:
        - rolling_avg: The rolling average of power
        - deviation: Difference from rolling average
        - is_anomaly: Boolean indicating if reading is abnormal
    
    Example:
        >>> df = pd.DataFrame({
        ...     'power_kw': [10, 11, 12, 11, 10, 50, 11, 10, 9]
        ... })
        >>> anomalies = detect_abnormal_spikes(df, window_size=3, deviation_threshold=2.0)
        >>> print(anomalies[['power_kw', 'rolling_avg', 'is_anomaly']])
    """
    # ========================================================================
    # Step 1: Make a copy to avoid modifying original data
    # ========================================================================
    data = df.copy()
    
    # ========================================================================
    # Step 2: Calculate rolling average
    # ========================================================================
    # rolling(window_size).mean() calculates average of last N readings
    # min_periods=1 means use available data even for first few rows
    data['rolling_avg'] = data[power_column].rolling(
        window=window_size,
        min_periods=1
    ).mean()
    
    # ========================================================================
    # Step 3: Calculate deviation from rolling average
    # ========================================================================
    # Positive deviation = reading is higher than trend (potential spike)
    # Negative deviation = reading is lower than trend
    data['deviation'] = data[power_column] - data['rolling_avg']
    
    # ========================================================================
    # Step 4: Calculate standard deviation of deviations
    # ========================================================================
    # This tells us how much variation from the trend is "normal"
    std_deviation = data['deviation'].std()
    
    # ========================================================================
    # Step 5: Mark readings as anomalies if deviation is too high
    # ========================================================================
    # If deviation > threshold * std_dev, it's an abnormal spike
    # deviation_threshold=2.0 means 2 standard deviations above normal
    data['is_anomaly'] = data['deviation'] > (deviation_threshold * std_deviation)
    
    # ========================================================================
    # Step 6: Return the result
    # ========================================================================
    return data


# ============================================================================
# SECTION 4: Combined Analysis Summary
# ============================================================================

def generate_analysis_report(
    df: pd.DataFrame,
    machine_id: str = None,
    power_column: str = 'power_kw',
    energy_column: str = 'energy_consumed_kwh'
) -> Dict:
    """
    Generate a comprehensive energy analysis report.
    
    This function combines all analysis methods to provide:
    - Daily consumption breakdown
    - Peak load statistics
    - Anomaly detection results
    - Overall summary
    
    Args:
        df: DataFrame with energy data
        machine_id: Optional machine identifier for report title
        power_column: Name of power column
        energy_column: Name of energy column
    
    Returns:
        Dictionary with complete analysis results
    """
    # ========================================================================
    # Calculate Daily Consumption
    # ========================================================================
    daily = calculate_daily_consumption(df, energy_column=energy_column)
    
    # ========================================================================
    # Identify Peak Periods
    # ========================================================================
    peaks = identify_peak_periods(df, power_column=power_column)
    
    # ========================================================================
    # Detect Anomalies
    # ========================================================================
    anomalies = detect_abnormal_spikes(df, power_column=power_column)
    anomaly_count = anomalies['is_anomaly'].sum()
    anomaly_percentage = (anomaly_count / len(anomalies)) * 100
    
    # ========================================================================
    # Build Report Dictionary
    # ========================================================================
    report = {
        'machine_id': machine_id or 'All Machines',
        'analysis_date': datetime.now().isoformat(),
        'data_points': len(df),
        
        'daily_consumption': {
            'total_days': len(daily),
            'average_daily_kwh': float(daily['total_energy_kwh'].mean()),
            'min_daily_kwh': float(daily['total_energy_kwh'].min()),
            'max_daily_kwh': float(daily['total_energy_kwh'].max()),
            'daily_data': daily.to_dict('records')
        },
        
        'peak_load': peaks,
        
        'anomalies': {
            'anomaly_count': int(anomaly_count),
            'anomaly_percentage': float(anomaly_percentage),
            'anomalous_readings': anomalies[anomalies['is_anomaly']][
                ['power_kw', 'rolling_avg', 'deviation']
            ].to_dict('records') if anomaly_count > 0 else []
        },
        
        'overall_statistics': {
            'average_power_kw': float(df[power_column].mean()),
            'min_power_kw': float(df[power_column].min()),
            'max_power_kw': float(df[power_column].max()),
            'std_deviation_kw': float(df[power_column].std()),
            'total_energy_kwh': float(df[energy_column].sum())
        }
    }
    
    return report


# ============================================================================
# SECTION 5: Example Usage and Testing
# ============================================================================

def example_usage():
    """
    Example showing how to use the analysis functions.
    """
    # Create sample data
    print("=" * 70)
    print("ENERGY DATA ANALYSIS - EXAMPLE")
    print("=" * 70)
    
    # Generate sample data: 48 hours of readings (every 30 minutes)
    timestamps = pd.date_range('2026-01-01', periods=48, freq='30min')
    np.random.seed(42)
    
    # Normal power usage with some variations
    base_power = 50
    power_data = base_power + np.random.normal(0, 5, 48)
    
    # Add some anomalies
    power_data[20] = 150  # Spike at position 20
    power_data[35] = 140  # Spike at position 35
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'power_kw': power_data,
        'energy_consumed_kwh': power_data / 2,  # Simplified calculation
        'machine_id': 'MACHINE-001'
    })
    
    print("\n1. SAMPLE DATA (first 10 rows):")
    print(df.head(10))
    
    # Daily consumption
    print("\n2. DAILY CONSUMPTION:")
    daily = calculate_daily_consumption(df)
    print(daily)
    
    # Peak periods
    print("\n3. PEAK LOAD ANALYSIS:")
    peaks = identify_peak_periods(df, percentile=75)
    for key, value in peaks.items():
        print(f"   {key}: {value}")
    
    # Anomaly detection
    print("\n4. ANOMALY DETECTION:")
    anomalies = detect_abnormal_spikes(df)
    anomalies_found = anomalies[anomalies['is_anomaly']]
    print(f"   Found {len(anomalies_found)} anomalies:")
    print(anomalies_found[['timestamp', 'power_kw', 'rolling_avg', 'deviation']])
    
    # Generate report
    print("\n5. COMPREHENSIVE REPORT:")
    report = generate_analysis_report(df, machine_id='MACHINE-001')
    print(f"   Machine: {report['machine_id']}")
    print(f"   Average Power: {report['overall_statistics']['average_power_kw']:.2f} kW")
    print(f"   Total Energy: {report['overall_statistics']['total_energy_kwh']:.2f} kWh")
    print(f"   Anomalies Found: {report['anomalies']['anomaly_count']}")
    
    print("\n" + "=" * 70)


# ============================================================================
# Run Example (only if this file is executed directly)
# ============================================================================

if __name__ == "__main__":
    example_usage()
