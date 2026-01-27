# Carbon Footprint Calculation Module for Smart Energy Platform
# Calculate CO2 emissions from energy consumption

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple

# ============================================================================
# EMISSION FACTORS (Based on Regional Grid Mix)
# ============================================================================
# These values represent how much CO2 is emitted per kilowatt-hour of
# electricity used on a given grid. Values vary by region based on energy mix.

# Standard US Average: ~0.385 kg CO2/kWh
# (Mix of coal, natural gas, renewable energy)
# Source: EPA, EIA

EMISSION_FACTORS_BY_REGION = {
    'US_Average': 0.385,        # kg CO2/kWh - US grid average
    'Coal_Heavy': 0.95,         # kg CO2/kWh - Coal-heavy region
    'Natural_Gas': 0.50,        # kg CO2/kWh - Natural gas dominant
    'Renewable_Heavy': 0.10,    # kg CO2/kWh - Renewable-heavy region
    'UK': 0.20,                 # kg CO2/kWh - UK grid
    'France': 0.06,             # kg CO2/kWh - France (mostly nuclear)
    'Germany': 0.38,            # kg CO2/kWh - Germany
    'India': 0.92,              # kg CO2/kWh - India
}

# Default emission factor (US Average)
DEFAULT_EMISSION_FACTOR = 0.385  # kg CO2/kWh

# ============================================================================
# FORMULA EXPLANATION
# ============================================================================
# 
# Basic Formula:
#   CO2 Emissions (kg) = Energy Consumption (kWh) × Emission Factor (kg CO2/kWh)
#
# Example:
#   Energy used: 100 kWh
#   Emission factor: 0.385 kg CO2/kWh
#   CO2 emissions = 100 × 0.385 = 38.5 kg CO2
#
# Breaking it down:
#   - Energy consumption is measured in kilowatt-hours (kWh)
#   - Emission factor tells us how much CO2 is released per unit of energy
#   - Different energy sources have different emission factors:
#     * Coal: high (~0.95 kg CO2/kWh)
#     * Natural gas: medium (~0.50 kg CO2/kWh)
#     * Renewables: very low (~0.01-0.10 kg CO2/kWh)
#     * Nuclear: very low (~0.01 kg CO2/kWh)
#
# Why it matters:
#   - Helps quantify environmental impact of energy usage
#   - Enables carbon reduction goals
#   - Used for sustainability reporting
#   - Helps identify opportunities to reduce emissions
#
# ============================================================================

def calculate_daily_co2_emissions(
    daily_energy_kwh: float,
    emission_factor: float = DEFAULT_EMISSION_FACTOR
) -> float:
    """
    Calculate CO2 emissions for a single day.
    
    Formula:
        Daily CO2 (kg) = Daily Energy (kWh) × Emission Factor (kg CO2/kWh)
    
    Args:
        daily_energy_kwh: Total energy consumed in one day (kilowatt-hours)
        emission_factor: kg CO2 per kWh (default: US average 0.385)
    
    Returns:
        float: CO2 emissions in kilograms for that day
    
    Example:
        >>> daily_co2 = calculate_daily_co2_emissions(1000)
        >>> print(f"{daily_co2:.2f} kg CO2")
        385.00 kg CO2
    
    Explanation:
        If a facility used 1000 kWh of electricity in a day,
        and the grid emission factor is 0.385 kg CO2/kWh,
        then the day's carbon footprint is: 1000 × 0.385 = 385 kg CO2
    """
    # ========================================================================
    # Calculation: Energy × Emission Factor
    # ========================================================================
    daily_co2 = daily_energy_kwh * emission_factor
    
    return daily_co2


def calculate_monthly_co2_emissions(
    daily_emissions_list: List[float]
) -> float:
    """
    Calculate total CO2 emissions for a month.
    
    Formula:
        Monthly CO2 (kg) = Sum of Daily CO2 Emissions
    
    Args:
        daily_emissions_list: List of daily CO2 emissions in kg
    
    Returns:
        float: Total CO2 emissions in kilograms for the month
    
    Example:
        >>> daily_emissions = [385, 400, 390, 395, 410]  # 5 days
        >>> monthly_co2 = calculate_monthly_co2_emissions(daily_emissions)
        >>> print(f"{monthly_co2:.2f} kg CO2")
        1980.00 kg CO2
    
    Explanation:
        Sum all daily emissions to get monthly total.
        This is the simplest aggregation method.
    """
    # ========================================================================
    # Calculation: Sum all daily values
    # ========================================================================
    monthly_co2 = sum(daily_emissions_list)
    
    return monthly_co2


def calculate_monthly_co2_from_dataframe(
    df: pd.DataFrame,
    energy_column: str = 'energy_consumed_kwh',
    emission_factor: float = DEFAULT_EMISSION_FACTOR
) -> Tuple[pd.DataFrame, float]:
    """
    Calculate daily and monthly CO2 emissions from a DataFrame.
    
    This function:
    1. Takes a DataFrame with energy data
    2. Calculates daily CO2 for each row
    3. Groups by date to get total daily CO2
    4. Sums all daily emissions for monthly total
    
    Args:
        df: DataFrame with timestamp and energy columns
        energy_column: Name of energy consumption column
        emission_factor: kg CO2 per kWh
    
    Returns:
        Tuple containing:
        - DataFrame: Daily CO2 breakdown (date, energy_kwh, co2_kg)
        - float: Monthly total CO2 in kilograms
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'timestamp': pd.date_range('2026-01-01', periods=48, freq='30min'),
        ...     'energy_consumed_kwh': [50] * 48
        ... })
        >>> daily_df, monthly_total = calculate_monthly_co2_from_dataframe(df)
        >>> print(daily_df)
        >>> print(f"Monthly Total: {monthly_total:.2f} kg CO2")
    """
    # ========================================================================
    # Step 1: Make a copy to avoid modifying original
    # ========================================================================
    data = df.copy()
    
    # ========================================================================
    # Step 2: Ensure timestamp is datetime
    # ========================================================================
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # ========================================================================
    # Step 3: Extract date (remove time component)
    # ========================================================================
    data['date'] = data['timestamp'].dt.date
    
    # ========================================================================
    # Step 4: Group by date and sum energy
    # ========================================================================
    daily_energy = data.groupby('date')[energy_column].sum().reset_index()
    daily_energy.columns = ['date', 'total_energy_kwh']
    
    # ========================================================================
    # Step 5: Calculate daily CO2 emissions
    # ========================================================================
    # Apply formula: CO2 = Energy × Emission Factor
    daily_energy['co2_kg'] = daily_energy['total_energy_kwh'] * emission_factor
    
    # ========================================================================
    # Step 6: Calculate monthly total
    # ========================================================================
    monthly_total_co2 = daily_energy['co2_kg'].sum()
    
    return daily_energy, monthly_total_co2


def calculate_co2_with_breakdown(
    df: pd.DataFrame,
    energy_column: str = 'energy_consumed_kwh',
    emission_factor: float = DEFAULT_EMISSION_FACTOR,
    region: str = 'US_Average'
) -> Dict:
    """
    Calculate comprehensive carbon footprint report.
    
    Provides:
    - Daily breakdown
    - Monthly summary
    - Comparison to common objects/activities
    - Reduction recommendations
    
    Args:
        df: Energy consumption DataFrame
        energy_column: Name of energy column
        emission_factor: kg CO2/kWh (overrides region if provided)
        region: Region name for context (e.g., 'US_Average')
    
    Returns:
        Dictionary with complete carbon footprint analysis
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({...})
        >>> report = calculate_co2_with_breakdown(df, region='US_Average')
        >>> print(report['summary']['monthly_co2_kg'])
    """
    # ========================================================================
    # Step 1: Calculate daily and monthly emissions
    # ========================================================================
    daily_df, monthly_co2 = calculate_monthly_co2_from_dataframe(
        df,
        energy_column=energy_column,
        emission_factor=emission_factor
    )
    
    # ========================================================================
    # Step 2: Calculate overall statistics
    # ========================================================================
    daily_averages = daily_df['co2_kg'].mean()
    daily_minimum = daily_df['co2_kg'].min()
    daily_maximum = daily_df['co2_kg'].max()
    
    # ========================================================================
    # Step 3: Convert to common units
    # ========================================================================
    # Convert kg to metric tonnes (1 tonne = 1000 kg)
    monthly_co2_tonnes = monthly_co2 / 1000
    
    # ========================================================================
    # Step 4: Calculate equivalent activities
    # ========================================================================
    # These are common equivalencies to help people understand impact
    
    # Driving a car: ~0.41 kg CO2 per km
    miles_driven_equivalent = (monthly_co2 / 0.41) * 0.621371  # km to miles
    
    # Tree absorbs: ~20 kg CO2 per year
    trees_needed_per_year = (monthly_co2 * 12) / 20
    
    # Average car produces: ~4.6 tonnes CO2 per year
    car_equivalent_months = (monthly_co2 / 1000) / (4.6 / 12)
    
    # ========================================================================
    # Step 5: Build comprehensive report
    # ========================================================================
    report = {
        'summary': {
            'region': region,
            'emission_factor_kg_per_kwh': emission_factor,
            'analysis_date': datetime.now().isoformat(),
            'total_days_analyzed': len(daily_df),
            'total_energy_kwh': daily_df['total_energy_kwh'].sum(),
            
            # Monthly emissions
            'monthly_co2_kg': float(monthly_co2),
            'monthly_co2_tonnes': float(monthly_co2_tonnes),
            
            # Daily statistics
            'daily_average_co2_kg': float(daily_averages),
            'daily_min_co2_kg': float(daily_minimum),
            'daily_max_co2_kg': float(daily_maximum),
        },
        
        'daily_breakdown': daily_df.to_dict('records'),
        
        'equivalencies': {
            'car_miles_equivalent': float(miles_driven_equivalent),
            'trees_needed_per_year': float(trees_needed_per_year),
            'car_months_equivalent': float(car_equivalent_months),
        },
        
        'formulas_used': {
            'daily_co2_kg': 'Energy (kWh) × Emission Factor (kg CO2/kWh)',
            'monthly_co2_kg': 'Sum of all daily CO2 emissions',
            'monthly_co2_tonnes': 'Monthly CO2 / 1000',
        },
        
        'insights': generate_insights(monthly_co2, daily_averages)
    }
    
    return report


def generate_insights(monthly_co2: float, daily_average: float) -> Dict:
    """
    Generate actionable insights about carbon emissions.
    
    Args:
        monthly_co2: Total monthly CO2 in kg
        daily_average: Average daily CO2 in kg
    
    Returns:
        Dictionary with observations and recommendations
    """
    insights = {
        'observations': [],
        'recommendations': []
    }
    
    # ========================================================================
    # Observation: Monthly total
    # ========================================================================
    if monthly_co2 > 50000:
        insights['observations'].append(
            f"High monthly emissions: {monthly_co2/1000:.1f} tonnes CO2"
        )
    elif monthly_co2 > 10000:
        insights['observations'].append(
            f"Moderate monthly emissions: {monthly_co2/1000:.1f} tonnes CO2"
        )
    else:
        insights['observations'].append(
            f"Low monthly emissions: {monthly_co2/1000:.1f} tonnes CO2"
        )
    
    # ========================================================================
    # Observation: Daily average
    # ========================================================================
    insights['observations'].append(
        f"Average daily emissions: {daily_average:.1f} kg CO2"
    )
    
    # ========================================================================
    # Recommendations
    # ========================================================================
    if daily_average > 500:
        insights['recommendations'].append(
            "Consider energy efficiency improvements (LED lights, HVAC optimization)"
        )
        insights['recommendations'].append(
            "Explore renewable energy options (solar, wind)"
        )
    
    if monthly_co2 > 30000:
        insights['recommendations'].append(
            "Implement demand management to reduce peak consumption"
        )
    
    insights['recommendations'].append(
        "Monitor consumption trends to identify anomalies"
    )
    
    return insights


def compare_emission_factors(energy_kwh: float) -> Dict:
    """
    Show how emissions vary by region/grid mix.
    
    Args:
        energy_kwh: Energy consumption in kWh
    
    Returns:
        Dictionary showing CO2 for each region
    
    Example:
        >>> comparison = compare_emission_factors(1000)
        >>> for region, co2 in comparison.items():
        ...     print(f"{region}: {co2:.2f} kg CO2")
    """
    comparison = {}
    
    for region, factor in EMISSION_FACTORS_BY_REGION.items():
        # ====================================================================
        # Formula: Energy × Regional Emission Factor
        # ====================================================================
        co2_kg = energy_kwh * factor
        comparison[region] = {
            'emission_factor': factor,
            'co2_kg': co2_kg,
            'percentage_of_us_average': (factor / DEFAULT_EMISSION_FACTOR) * 100
        }
    
    return comparison


# ============================================================================
# EXAMPLE: How to Use These Functions
# ============================================================================

def example_carbon_calculation():
    """
    Demonstrates carbon footprint calculations with sample data.
    """
    print("\n" + "=" * 70)
    print("CARBON FOOTPRINT CALCULATION EXAMPLE")
    print("=" * 70)
    
    # ========================================================================
    # Example 1: Single Day Calculation
    # ========================================================================
    print("\n1. SINGLE DAY CALCULATION")
    print("-" * 70)
    
    daily_energy = 500  # kWh
    daily_co2 = calculate_daily_co2_emissions(daily_energy)
    
    print(f"Energy consumed: {daily_energy} kWh")
    print(f"Emission factor: {DEFAULT_EMISSION_FACTOR} kg CO2/kWh")
    print(f"Daily CO2 emissions: {daily_co2:.2f} kg")
    print(f"                   = {daily_co2/1000:.3f} tonnes")
    
    # ========================================================================
    # Example 2: Monthly Calculation
    # ========================================================================
    print("\n2. MONTHLY CALCULATION")
    print("-" * 70)
    
    daily_energy_values = [500, 520, 480, 550, 490, 510, 495]  # 7 days
    daily_emissions = [calculate_daily_co2_emissions(e) for e in daily_energy_values]
    
    monthly_co2 = calculate_monthly_co2_emissions(daily_emissions)
    
    print("Daily energy consumption:")
    for day, energy in enumerate(daily_energy_values, 1):
        print(f"  Day {day}: {energy} kWh → {energy * DEFAULT_EMISSION_FACTOR:.1f} kg CO2")
    
    print(f"\nMonthly total: {monthly_co2:.2f} kg CO2 ({monthly_co2/1000:.3f} tonnes)")
    
    # ========================================================================
    # Example 3: Regional Comparison
    # ========================================================================
    print("\n3. REGIONAL EMISSION COMPARISON")
    print("-" * 70)
    print(f"For 1000 kWh of energy consumption:\n")
    
    comparison = compare_emission_factors(1000)
    for region, data in sorted(comparison.items(), key=lambda x: x[1]['co2_kg']):
        print(f"  {region:20} {data['co2_kg']:6.1f} kg CO2  "
              f"({data['percentage_of_us_average']:5.1f}% of US avg)")
    
    # ========================================================================
    # Example 4: DataFrame Analysis
    # ========================================================================
    print("\n4. DATAFRAME ANALYSIS")
    print("-" * 70)
    
    # Create sample data
    df = pd.DataFrame({
        'timestamp': pd.date_range('2026-01-01', periods=48, freq='30min'),
        'energy_consumed_kwh': np.random.normal(50, 10, 48)
    })
    
    # Make sure all values are positive
    df['energy_consumed_kwh'] = df['energy_consumed_kwh'].abs()
    
    daily_df, monthly_total = calculate_monthly_co2_from_dataframe(df)
    
    print("Daily CO2 Breakdown (first 3 days):")
    print(daily_df.head(3).to_string(index=False))
    print(f"\nMonthly Total: {monthly_total:.2f} kg CO2")
    
    # ========================================================================
    # Example 5: Comprehensive Report
    # ========================================================================
    print("\n5. COMPREHENSIVE CARBON FOOTPRINT REPORT")
    print("-" * 70)
    
    report = calculate_co2_with_breakdown(df, region='US_Average')
    
    summary = report['summary']
    print(f"Region: {summary['region']}")
    print(f"Total Energy: {summary['total_energy_kwh']:.1f} kWh")
    print(f"Monthly CO2: {summary['monthly_co2_kg']:.1f} kg ({summary['monthly_co2_tonnes']:.3f} tonnes)")
    print(f"Daily Average: {summary['daily_average_co2_kg']:.1f} kg CO2")
    print(f"Daily Range: {summary['daily_min_co2_kg']:.1f} - {summary['daily_max_co2_kg']:.1f} kg CO2")
    
    print(f"\nEquivalencies:")
    equiv = report['equivalencies']
    print(f"  = {equiv['car_miles_equivalent']:.0f} miles of car driving")
    print(f"  = {equiv['trees_needed_per_year']:.0f} trees needed/year to offset")
    print(f"  = {equiv['car_months_equivalent']:.1f} months of car emissions")
    
    print(f"\nInsights:")
    for obs in report['insights']['observations']:
        print(f"  • {obs}")
    
    print(f"\nRecommendations:")
    for rec in report['insights']['recommendations']:
        print(f"  → {rec}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_carbon_calculation()
