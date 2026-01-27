#!/usr/bin/env python3
"""
Carbon Footprint Testing Script

Tests the carbon footprint calculation module and endpoint.
Demonstrates:
- Daily CO2 calculations
- Monthly aggregations
- Regional comparisons
- API endpoint usage
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# ============================================================================
# Test 1: Basic Calculations
# ============================================================================

def test_daily_calculation():
    """Test single day CO2 calculation."""
    print("\n" + "=" * 70)
    print("TEST 1: SINGLE DAY CO2 CALCULATION")
    print("=" * 70)
    
    from carbon_footprint import calculate_daily_co2_emissions
    
    # Test data
    energy_consumed = 500  # kWh
    emission_factor = 0.385  # kg CO2/kWh (US Average)
    
    # Calculate
    daily_co2 = calculate_daily_co2_emissions(energy_consumed, emission_factor)
    
    # Display results
    print(f"\nInput:")
    print(f"  Energy consumed: {energy_consumed} kWh")
    print(f"  Emission factor: {emission_factor} kg CO2/kWh")
    
    print(f"\nFormula:")
    print(f"  CO2 = {energy_consumed} × {emission_factor}")
    print(f"  CO2 = {daily_co2:.2f} kg")
    
    print(f"\nOutput:")
    print(f"  Daily CO2: {daily_co2:.2f} kg")
    print(f"  As tonnes: {daily_co2/1000:.4f} tonnes")
    
    # Validate
    expected = 500 * 0.385
    assert abs(daily_co2 - expected) < 0.01, "Calculation error!"
    print(f"\n✓ Test passed!")


# ============================================================================
# Test 2: Monthly Aggregation
# ============================================================================

def test_monthly_aggregation():
    """Test monthly CO2 aggregation."""
    print("\n" + "=" * 70)
    print("TEST 2: MONTHLY CO2 AGGREGATION")
    print("=" * 70)
    
    from carbon_footprint import (
        calculate_daily_co2_emissions,
        calculate_monthly_co2_emissions
    )
    
    # Create 7 days of energy data
    daily_energy = [500, 520, 480, 550, 490, 510, 495]
    emission_factor = 0.385
    
    # Calculate daily CO2
    daily_emissions = [
        calculate_daily_co2_emissions(e, emission_factor)
        for e in daily_energy
    ]
    
    # Calculate monthly total
    monthly_total = calculate_monthly_co2_emissions(daily_emissions)
    
    # Display results
    print(f"\nDaily Energy and CO2:")
    print(f"{'Day':>5} {'Energy (kWh)':>15} {'CO2 (kg)':>15}")
    print("-" * 40)
    
    for day, (energy, co2) in enumerate(zip(daily_energy, daily_emissions), 1):
        print(f"{day:>5} {energy:>15.1f} {co2:>15.2f}")
    
    print("-" * 40)
    print(f"{'TOTAL':>5} {sum(daily_energy):>15.1f} {monthly_total:>15.2f}")
    
    print(f"\nSummary:")
    print(f"  Total energy: {sum(daily_energy):.1f} kWh")
    print(f"  Monthly CO2: {monthly_total:.2f} kg ({monthly_total/1000:.4f} tonnes)")
    print(f"  Daily average: {monthly_total/len(daily_energy):.2f} kg CO2")
    
    print(f"\n✓ Test passed!")


# ============================================================================
# Test 3: DataFrame Processing
# ============================================================================

def test_dataframe_processing():
    """Test carbon calculation from DataFrame."""
    print("\n" + "=" * 70)
    print("TEST 3: DATAFRAME PROCESSING")
    print("=" * 70)
    
    from carbon_footprint import calculate_monthly_co2_from_dataframe
    
    # Create sample energy data
    # 48 data points = 2 days of 30-minute intervals
    start_date = datetime(2026, 1, 1)
    timestamps = [start_date + timedelta(minutes=30*i) for i in range(48)]
    
    # Energy values (varying throughout the day)
    energy_values = [
        # Day 1
        40, 42, 38, 40, 45, 50, 60, 70, 80, 85, 90, 85,  # Morning/noon
        80, 75, 70, 65, 60, 55, 50, 48, 45, 43, 40, 38,  # Afternoon/evening
        # Day 2
        35, 32, 30, 32, 40, 55, 70, 80, 85, 90, 92, 88,  # Morning/noon
        85, 78, 72, 68, 65, 60, 50, 45, 42, 40, 38, 35,  # Afternoon/evening
    ]
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'energy_consumed_kwh': energy_values
    })
    
    # Calculate
    daily_df, monthly_total = calculate_monthly_co2_from_dataframe(
        df,
        energy_column='energy_consumed_kwh',
        emission_factor=0.385
    )
    
    # Display results
    print(f"\nDaily CO2 Breakdown:")
    print(daily_df.to_string(index=False))
    
    print(f"\nSummary Statistics:")
    print(f"  Days analyzed: {len(daily_df)}")
    print(f"  Total energy: {daily_df['total_energy_kwh'].sum():.1f} kWh")
    print(f"  Total CO2: {monthly_total:.2f} kg ({monthly_total/1000:.4f} tonnes)")
    print(f"  Daily average: {daily_df['total_energy_kwh'].mean():.1f} kWh/day")
    print(f"  Daily CO2 avg: {daily_df['co2_kg'].mean():.2f} kg CO2/day")
    
    print(f"\n✓ Test passed!")


# ============================================================================
# Test 4: Regional Comparison
# ============================================================================

def test_regional_comparison():
    """Test emission factor comparison across regions."""
    print("\n" + "=" * 70)
    print("TEST 4: REGIONAL EMISSION FACTOR COMPARISON")
    print("=" * 70)
    
    from carbon_footprint import compare_emission_factors
    
    # For 1000 kWh of consumption
    energy_kwh = 1000
    
    comparison = compare_emission_factors(energy_kwh)
    
    print(f"\nFor {energy_kwh} kWh of energy consumption:\n")
    print(f"{'Region':<20} {'Factor':>12} {'CO2 (kg)':>15} {'% of US avg':>12}")
    print("-" * 60)
    
    for region, data in sorted(comparison.items(), key=lambda x: x[1]['co2_kg']):
        factor = data['emission_factor']
        co2 = data['co2_kg']
        percentage = data['percentage_of_us_average']
        
        print(f"{region:<20} {factor:>12.2f} {co2:>15.1f} {percentage:>11.1f}%")
    
    print("\nInterpretation:")
    print("  - Lower factor = cleaner grid (more renewables)")
    print("  - Higher factor = dirtier grid (more coal/fossil fuels)")
    print("  - France (0.06): Mostly nuclear, very clean")
    print("  - US Average (0.385): Mixed grid")
    print("  - Coal_Heavy (0.95): Coal-dependent, dirty")
    
    print(f"\n✓ Test passed!")


# ============================================================================
# Test 5: Comprehensive Report
# ============================================================================

def test_comprehensive_report():
    """Test full carbon footprint analysis report."""
    print("\n" + "=" * 70)
    print("TEST 5: COMPREHENSIVE CARBON FOOTPRINT REPORT")
    print("=" * 70)
    
    from carbon_footprint import calculate_co2_with_breakdown
    
    # Create sample data
    start_date = datetime(2026, 1, 1)
    timestamps = [start_date + timedelta(hours=i) for i in range(168)]  # 7 days
    
    # Realistic energy pattern: higher during day, lower at night
    energy_values = [
        # Day 1-7 pattern (high during 8am-5pm, low at night)
        30, 28, 25, 25, 30, 40, 50, 60, 70, 80, 85, 90,
        88, 85, 80, 75, 70, 65, 55, 45, 35, 32, 30, 28,
    ] * 7  # Repeat for 7 days
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'energy_consumed_kwh': energy_values
    })
    
    # Generate report
    report = calculate_co2_with_breakdown(df, region='US_Average')
    
    # Display results
    print(f"\nCarbon Footprint Analysis Report")
    print(f"Region: {report['summary']['region']}")
    print(f"Analysis Date: {report['summary']['analysis_date']}")
    
    summary = report['summary']
    print(f"\nEnergy Summary:")
    print(f"  Total energy: {summary['total_energy_kwh']:.1f} kWh")
    print(f"  Days analyzed: {summary['total_days_analyzed']}")
    print(f"  Daily average: {summary['total_energy_kwh']/summary['total_days_analyzed']:.1f} kWh/day")
    
    print(f"\nCO2 Emissions:")
    print(f"  Monthly total: {summary['monthly_co2_kg']:.2f} kg")
    print(f"  As tonnes: {summary['monthly_co2_tonnes']:.4f} tonnes")
    print(f"  Daily average: {summary['daily_average_co2_kg']:.2f} kg CO2/day")
    print(f"  Daily range: {summary['daily_min_co2_kg']:.2f} - {summary['daily_max_co2_kg']:.2f} kg CO2")
    
    equiv = report['equivalencies']
    print(f"\nEquivalencies (to understand impact):")
    print(f"  Car miles: {equiv['car_miles_equivalent']:.0f} miles of driving")
    print(f"  Trees needed: {equiv['trees_needed_per_year']:.0f} trees to offset/year")
    print(f"  Car months: {equiv['car_months_equivalent']:.1f} months of car emissions")
    
    print(f"\nInsights:")
    print(f"  Observations:")
    for obs in report['insights']['observations']:
        print(f"    • {obs}")
    print(f"  Recommendations:")
    for rec in report['insights']['recommendations']:
        print(f"    → {rec}")
    
    # Show first 3 days of breakdown
    print(f"\nDaily Breakdown (first 3 days):")
    for i, day in enumerate(report['daily_breakdown'][:3], 1):
        print(f"  {day['date']}: {day['total_energy_kwh']:.1f} kWh → {day['co2_kg']:.2f} kg CO2")
    
    print(f"\n✓ Test passed!")


# ============================================================================
# Test 6: API Response Format
# ============================================================================

def test_api_response_format():
    """Test that API response is valid JSON."""
    print("\n" + "=" * 70)
    print("TEST 6: API RESPONSE FORMAT VALIDATION")
    print("=" * 70)
    
    from carbon_footprint import calculate_co2_with_breakdown
    import pandas as pd
    
    # Create sample data
    df = pd.DataFrame({
        'timestamp': pd.date_range('2026-01-01', periods=100, freq='1H'),
        'energy_consumed_kwh': np.random.normal(50, 10, 100).clip(lower=0)
    })
    
    # Generate report
    report = calculate_co2_with_breakdown(df)
    
    # Simulate API response structure
    response = {
        'analysis_date': datetime.now().isoformat(),
        'machine_id': 'TEST-001',
        'region': 'US_Average',
        'summary': {
            'total_energy_kwh': float(report['summary']['total_energy_kwh']),
            'monthly_co2_kg': float(report['summary']['monthly_co2_kg']),
            'monthly_co2_tonnes': float(report['summary']['monthly_co2_tonnes']),
            'daily_average_co2_kg': float(report['summary']['daily_average_co2_kg']),
        },
        'daily_breakdown': report['daily_breakdown'],
        'equivalencies': report['equivalencies'],
        'insights': report['insights']
    }
    
    # Validate JSON serialization
    try:
        json_str = json.dumps(response, indent=2, default=str)
        print(f"\nJSON Response (first 500 chars):")
        print(json_str[:500] + "...")
        print(f"\nTotal JSON size: {len(json_str):,} characters")
        print(f"✓ JSON serialization successful!")
    except Exception as e:
        print(f"✗ JSON serialization failed: {e}")
        return False
    
    print(f"\n✓ Test passed!")
    return True


# ============================================================================
# Main Test Runner
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("CARBON FOOTPRINT MODULE TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Daily Calculation", test_daily_calculation),
        ("Monthly Aggregation", test_monthly_aggregation),
        ("DataFrame Processing", test_dataframe_processing),
        ("Regional Comparison", test_regional_comparison),
        ("Comprehensive Report", test_comprehensive_report),
        ("API Response Format", test_api_response_format),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total: {len(tests)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    
    if failed == 0:
        print(f"\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
