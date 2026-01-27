#!/usr/bin/env python3
"""
Test script for /sustainability/carbon endpoint

This script tests the new beginner-friendly carbon emissions endpoint.
Run this after starting the FastAPI server with: python main.py
"""

import requests
import json
from datetime import datetime, timedelta

# ============================================================================
# Configuration
# ============================================================================
API_URL = "http://127.0.0.1:8000"
SUSTAINABILITY_ENDPOINT = f"{API_URL}/sustainability/carbon"
ENERGY_ADD_ENDPOINT = f"{API_URL}/energy/add"

# ============================================================================
# Test 1: Add Sample Energy Data
# ============================================================================

def test_add_sample_data():
    """Add sample energy readings to the database."""
    print("\n" + "=" * 70)
    print("TEST 1: Adding Sample Energy Data")
    print("=" * 70)
    
    # Create 5 sample readings for testing
    readings = [
        {"machine_id": "TEST-PUMP", "power_kw": 50.5, "energy_consumed_kwh": 100.0},
        {"machine_id": "TEST-PUMP", "power_kw": 52.0, "energy_consumed_kwh": 104.0},
        {"machine_id": "TEST-PUMP", "power_kw": 48.5, "energy_consumed_kwh": 97.0},
        {"machine_id": "TEST-COMPRESSOR", "power_kw": 75.0, "energy_consumed_kwh": 150.0},
        {"machine_id": "TEST-COMPRESSOR", "power_kw": 72.5, "energy_consumed_kwh": 145.0},
    ]
    
    for reading in readings:
        try:
            response = requests.post(ENERGY_ADD_ENDPOINT, json=reading)
            
            if response.status_code == 201:
                print(f"✓ Added: {reading['machine_id']} - {reading['energy_consumed_kwh']} kWh")
            else:
                print(f"✗ Failed: {reading['machine_id']} - Status {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    print(f"\nTotal readings added: {len(readings)}")

# ============================================================================
# Test 2: Get Emissions for All Machines
# ============================================================================

def test_all_machines():
    """Test carbon emissions for all machines combined."""
    print("\n" + "=" * 70)
    print("TEST 2: Carbon Emissions - All Machines")
    print("=" * 70)
    
    try:
        response = requests.get(SUSTAINABILITY_ENDPOINT)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Request successful (200 OK)")
            
            # Display results
            print(f"\nEmissions:")
            print(f"  Total CO2: {data['emissions']['total_kg_co2']:.2f} kg")
            print(f"  As tonnes: {data['emissions']['total_tonnes_co2']:.4f} tonnes")
            print(f"  Factor: {data['emissions']['emission_factor_used']}")
            
            print(f"\nEnergy:")
            print(f"  Total: {data['energy']['total_kwh']:.1f} kWh")
            print(f"  Daily average: {data['energy']['daily_average_kwh']:.1f} kWh")
            print(f"  Daily CO2 avg: {data['energy']['daily_average_co2_kg']:.2f} kg")
            
            print(f"\nEquivalencies:")
            print(f"  Car miles: {data['equivalencies']['car_miles']:.0f} miles")
            print(f"  {data['equivalencies']['description']}")
            
            print(f"\nMetadata:")
            print(f"  Data points: {data['metadata']['data_points']}")
            print(f"  Days: {data['metadata']['days_analyzed']}")
            print(f"  Machine: {data['metadata']['machine_id']}")
            
            return data
        else:
            print(f"✗ Request failed: Status {response.status_code}")
            print(f"  Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Connection error: Is the server running?")
        print(f"  Start with: python main.py")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

# ============================================================================
# Test 3: Get Emissions for Specific Machine
# ============================================================================

def test_specific_machine(machine_id="TEST-PUMP"):
    """Test carbon emissions for a specific machine."""
    print("\n" + "=" * 70)
    print(f"TEST 3: Carbon Emissions - Machine '{machine_id}'")
    print("=" * 70)
    
    try:
        response = requests.get(SUSTAINABILITY_ENDPOINT, params={"machine_id": machine_id})
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Request successful (200 OK)")
            
            print(f"\nResults for {machine_id}:")
            print(f"  Total CO2: {data['emissions']['total_kg_co2']:.2f} kg")
            print(f"  As tonnes: {data['emissions']['total_tonnes_co2']:.4f} tonnes")
            print(f"  Car miles: {data['equivalencies']['car_miles']:.0f} miles")
            print(f"  Data points: {data['metadata']['data_points']}")
            
            return data
        else:
            print(f"✗ Request failed: Status {response.status_code}")
            print(f"  Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

# ============================================================================
# Test 4: Test Error Case - Nonexistent Machine
# ============================================================================

def test_error_case():
    """Test that endpoint properly handles no data (404)."""
    print("\n" + "=" * 70)
    print("TEST 4: Error Handling - Nonexistent Machine")
    print("=" * 70)
    
    try:
        response = requests.get(
            SUSTAINABILITY_ENDPOINT,
            params={"machine_id": "NONEXISTENT-MACHINE"}
        )
        
        if response.status_code == 404:
            print(f"✓ Correctly returned 404 Not Found")
            error = response.json()
            print(f"  Message: {error['detail']}")
            return True
        else:
            print(f"✗ Expected 404, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

# ============================================================================
# Test 5: Validate Response Structure
# ============================================================================

def test_response_structure(data):
    """Validate that response has all required fields."""
    print("\n" + "=" * 70)
    print("TEST 5: Response Structure Validation")
    print("=" * 70)
    
    required_fields = {
        'status': str,
        'emissions': dict,
        'energy': dict,
        'equivalencies': dict,
        'metadata': dict
    }
    
    nested_fields = {
        'emissions': ['total_kg_co2', 'total_tonnes_co2', 'emission_factor_used'],
        'energy': ['total_kwh', 'daily_average_kwh', 'daily_average_co2_kg'],
        'equivalencies': ['car_miles', 'description'],
        'metadata': ['data_points', 'days_analyzed', 'machine_id']
    }
    
    print("\nChecking required fields...")
    all_valid = True
    
    # Check top-level fields
    for field, field_type in required_fields.items():
        if field in data:
            if isinstance(data[field], field_type):
                print(f"  ✓ {field}: Present and correct type")
            else:
                print(f"  ✗ {field}: Wrong type (expected {field_type.__name__})")
                all_valid = False
        else:
            print(f"  ✗ {field}: Missing")
            all_valid = False
    
    # Check nested fields
    print("\nChecking nested fields...")
    for section, fields in nested_fields.items():
        for field in fields:
            if section in data and field in data[section]:
                print(f"  ✓ {section}.{field}: Present")
            else:
                print(f"  ✗ {section}.{field}: Missing")
                all_valid = False
    
    if all_valid:
        print(f"\n✓ All fields valid!")
    else:
        print(f"\n✗ Some fields missing or incorrect")
    
    return all_valid

# ============================================================================
# Test 6: Verify Calculation Accuracy
# ============================================================================

def test_calculation(data):
    """Verify CO2 calculation is correct."""
    print("\n" + "=" * 70)
    print("TEST 6: Calculation Accuracy")
    print("=" * 70)
    
    # Expected: Energy × 0.385 = CO2
    emission_factor = 0.385
    
    total_kwh = data['energy']['total_kwh']
    expected_co2 = total_kwh * emission_factor
    actual_co2 = data['emissions']['total_kg_co2']
    
    # Check if calculation is correct (within 0.1 kg tolerance)
    difference = abs(expected_co2 - actual_co2)
    tolerance = 0.1
    
    print(f"\nFormula Verification:")
    print(f"  Total Energy: {total_kwh:.1f} kWh")
    print(f"  Emission Factor: {emission_factor} kg CO2/kWh")
    print(f"  Expected CO2: {expected_co2:.2f} kg")
    print(f"  Actual CO2: {actual_co2:.2f} kg")
    print(f"  Difference: {difference:.2f} kg")
    
    if difference <= tolerance:
        print(f"\n✓ Calculation is CORRECT (within {tolerance} kg tolerance)")
        return True
    else:
        print(f"\n✗ Calculation is INCORRECT (difference > {tolerance} kg)")
        return False

# ============================================================================
# Main Test Runner
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("SUSTAINABILITY CARBON ENDPOINT TEST SUITE")
    print("=" * 70)
    print(f"\nAPI URL: {API_URL}")
    print(f"Endpoint: /sustainability/carbon")
    
    results = {
        'add_data': False,
        'all_machines': False,
        'specific_machine': False,
        'error_handling': False,
        'response_structure': False,
        'calculation': False
    }
    
    # Test 1: Add data
    test_add_sample_data()
    results['add_data'] = True
    
    # Test 2: All machines
    all_data = test_all_machines()
    if all_data:
        results['all_machines'] = True
        
        # Test 5: Response structure
        results['response_structure'] = test_response_structure(all_data)
        
        # Test 6: Calculation
        results['calculation'] = test_calculation(all_data)
    
    # Test 3: Specific machine
    pump_data = test_specific_machine("TEST-PUMP")
    if pump_data:
        results['specific_machine'] = True
    
    # Test 4: Error handling
    results['error_handling'] = test_error_case()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, status in results.items():
        status_str = "✓ PASS" if status else "✗ FAIL"
        print(f"{test:30} {status_str}")
    
    print(f"\n{'Total':30} {passed}/{total} passed")
    
    if passed == total:
        print(f"\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
