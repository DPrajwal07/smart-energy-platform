#!/usr/bin/env python3
# Test script for the /analytics/daily endpoint
# This demonstrates how to use the new analytics endpoint

import requests
import json
from datetime import datetime, timedelta

# ============================================================================
# Configuration
# ============================================================================
API_BASE_URL = "http://127.0.0.1:8000"
ANALYTICS_ENDPOINT = f"{API_BASE_URL}/analytics/daily"

# ============================================================================
# Function: Test Analytics Endpoint
# ============================================================================
def test_analytics_endpoint():
    """
    Test the /analytics/daily endpoint with different parameters.
    """
    print("\n" + "=" * 70)
    print("TESTING /analytics/daily ENDPOINT")
    print("=" * 70)
    
    # ========================================================================
    # Test 1: Get analytics for all machines
    # ========================================================================
    print("\n1. GET DAILY ANALYTICS FOR ALL MACHINES")
    print("-" * 70)
    
    try:
        response = requests.get(ANALYTICS_ENDPOINT)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Request successful (HTTP 200)")
            print(f"\n  Machine(s): {data['machine_id']}")
            print(f"  Data points: {data['data_points']}")
            print(f"  Analysis date: {data['analysis_date']}")
            print(f"\n  Summary Statistics:")
            print(f"    Average daily consumption: {data['summary']['average_daily_kwh']:.2f} kWh")
            print(f"    Minimum daily consumption: {data['summary']['min_daily_kwh']:.2f} kWh")
            print(f"    Maximum daily consumption: {data['summary']['max_daily_kwh']:.2f} kWh")
            print(f"    Total days analyzed: {data['summary']['total_days']}")
            
            if data['daily_data']:
                print(f"\n  Daily Breakdown (first 3 days):")
                for day in data['daily_data'][:3]:
                    print(f"    {day['date']}: {day['total_energy_kwh']:.2f} kWh")
        
        elif response.status_code == 404:
            print(f"✗ No data found (HTTP 404)")
            print(f"  Message: {response.json()['detail']}")
            print(f"\n  Tip: Add energy readings first using /energy/add endpoint")
        
        else:
            print(f"✗ Error (HTTP {response.status_code})")
            print(f"  Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("✗ Connection error - Is the server running?")
        print(f"  Make sure the API is running at {API_BASE_URL}")
        return
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # ========================================================================
    # Test 2: Get analytics for a specific machine
    # ========================================================================
    print("\n2. GET DAILY ANALYTICS FOR SPECIFIC MACHINE")
    print("-" * 70)
    
    machine_id = "MACHINE-001"
    params = {"machine_id": machine_id}
    
    try:
        response = requests.get(ANALYTICS_ENDPOINT, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Request successful (HTTP 200)")
            print(f"\n  Machine: {data['machine_id']}")
            print(f"  Data points: {data['data_points']}")
            print(f"\n  Summary for {machine_id}:")
            print(f"    Average: {data['summary']['average_daily_kwh']:.2f} kWh/day")
            print(f"    Range: {data['summary']['min_daily_kwh']:.2f} - {data['summary']['max_daily_kwh']:.2f} kWh")
        
        elif response.status_code == 404:
            print(f"✗ No data found for {machine_id}")
            print(f"  Try adding data first or query a different machine")
        
        else:
            print(f"✗ Error (HTTP {response.status_code})")
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # ========================================================================
    # Test 3: Pretty print full response
    # ========================================================================
    print("\n3. FULL JSON RESPONSE (ALL MACHINES)")
    print("-" * 70)
    
    try:
        response = requests.get(ANALYTICS_ENDPOINT)
        
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2, default=str))
        else:
            print(f"Could not retrieve data (HTTP {response.status_code})")
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("\n" + "=" * 70)

# ============================================================================
# Function: Add Sample Data
# ============================================================================
def add_sample_data():
    """
    Add sample energy data to test the analytics endpoint.
    """
    print("\n" + "=" * 70)
    print("ADDING SAMPLE DATA FOR TESTING")
    print("=" * 70)
    
    # Sample readings for testing
    test_readings = [
        {"machine_id": "MACHINE-001", "power_kw": 45.5, "energy_consumed_kwh": 1250.75},
        {"machine_id": "MACHINE-001", "power_kw": 52.3, "energy_consumed_kwh": 1400.20},
        {"machine_id": "MACHINE-002", "power_kw": 38.1, "energy_consumed_kwh": 980.50},
        {"machine_id": "MACHINE-002", "power_kw": 41.7, "energy_consumed_kwh": 1050.30},
    ]
    
    added_count = 0
    
    for reading in test_readings:
        try:
            response = requests.post(
                f"{API_BASE_URL}/energy/add",
                json=reading
            )
            
            if response.status_code == 201:
                print(f"✓ Added: {reading['machine_id']} - {reading['power_kw']} kW")
                added_count += 1
            else:
                print(f"✗ Failed: {reading['machine_id']} (HTTP {response.status_code})")
        
        except Exception as e:
            print(f"✗ Error adding data: {str(e)}")
    
    print(f"\nTotal added: {added_count}/{len(test_readings)}")
    print("=" * 70)

# ============================================================================
# Main Function
# ============================================================================
def main():
    """
    Main test function.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Smart Energy Platform - Analytics Endpoint Test".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Try to add sample data first
    response = requests.get(ANALYTICS_ENDPOINT)
    if response.status_code == 404:
        print("\nNo data found. Would you like to add sample data first?")
        add_sample_data()
    
    # Test the endpoint
    test_analytics_endpoint()
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    print("\nEndpoint URL: GET /analytics/daily")
    print("Optional parameter: ?machine_id=MACHINE-001")
    print(f"\nFull URL: {ANALYTICS_ENDPOINT}")
    print(f"With parameter: {ANALYTICS_ENDPOINT}?machine_id=MACHINE-001")
    print("\n" + "=" * 70 + "\n")

# ============================================================================
# Run Tests
# ============================================================================
if __name__ == "__main__":
    main()
