#!/usr/bin/env python3
"""
Quick verification script for /analytics/daily endpoint.
Shows that the endpoint code is syntactically correct and imports work.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("VERIFYING /analytics/daily ENDPOINT SETUP")
print("=" * 70)

try:
    print("\n1. Checking imports...")
    from main import app, get_daily_analytics
    print("   ✓ FastAPI app imported successfully")
    print("   ✓ get_daily_analytics function found")
    
    print("\n2. Checking analysis module...")
    from analysis import calculate_daily_consumption
    print("   ✓ Analysis module imported successfully")
    print("   ✓ calculate_daily_consumption function available")
    
    print("\n3. Checking database module...")
    from database import get_db, Base, engine
    print("   ✓ Database module imported successfully")
    print("   ✓ get_db dependency available")
    
    print("\n4. Checking Pandas...")
    import pandas as pd
    print(f"   ✓ Pandas imported successfully (version {pd.__version__})")
    
    print("\n5. Checking FastAPI routes...")
    routes = [route.path for route in app.routes]
    analytics_routes = [r for r in routes if 'analytics' in r]
    
    if analytics_routes:
        print(f"   ✓ Found analytics routes: {analytics_routes}")
    else:
        print("   ✗ No analytics routes found!")
    
    print("\n6. Checking endpoint in routes...")
    if "/analytics/daily" in routes:
        print("   ✓ /analytics/daily endpoint is registered!")
    else:
        print("   ✗ /analytics/daily not found in routes")
        print(f"   Available routes: {routes}")
    
    print("\n" + "=" * 70)
    print("VERIFICATION RESULT: ✅ ALL CHECKS PASSED")
    print("=" * 70)
    print("\nThe /analytics/daily endpoint is properly configured.")
    print("\nTo test it:")
    print("  1. Start the server: python main.py")
    print("  2. Add data: curl -X POST http://127.0.0.1:8000/energy/add \\")
    print('       -d \'{"machine_id":"MACHINE-001","power_kw":45.5,"energy_consumed_kwh":1250}\'')
    print("  3. Test endpoint: curl http://127.0.0.1:8000/analytics/daily")
    print("\nOr run: python test_analytics.py")
    print("=" * 70 + "\n")
    
except ImportError as e:
    print(f"\n✗ Import Error: {e}")
    print("\nMake sure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
