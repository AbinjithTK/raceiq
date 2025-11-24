"""Test real data integration - verify all endpoints work with actual CSV data"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url, expected_keys):
    """Test an API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print('-'*60)
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Status: {response.status_code}")
            print(f"Response keys: {list(data.keys())}")
            
            # Check expected keys
            missing = [k for k in expected_keys if k not in data]
            if missing:
                print(f"⚠️  Missing keys: {missing}")
            else:
                print(f"✅ All expected keys present")
            
            # Show sample data
            for key in expected_keys[:3]:  # Show first 3 keys
                if key in data:
                    value = data[key]
                    if isinstance(value, list):
                        print(f"  {key}: [{len(value)} items]")
                        if value:
                            print(f"    Sample: {value[0]}")
                    else:
                        print(f"  {key}: {value}")
            
            return True
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("REAL DATA INTEGRATION TEST")
    print("="*60)
    
    tests = [
        {
            "name": "Live Telemetry",
            "url": f"{BASE_URL}/api/telemetry/live/barber/1/78?lap=5",
            "keys": ["track", "race", "vehicle", "lap", "points", "total_points"]
        },
        {
            "name": "Optimal Telemetry",
            "url": f"{BASE_URL}/api/telemetry/optimal/barber/1",
            "keys": ["avg_speed", "max_speed", "avg_throttle", "avg_brake", "lap_time"]
        },
        {
            "name": "Telemetry Comparison",
            "url": f"{BASE_URL}/api/telemetry/comparison/barber/1/78?lap=5",
            "keys": ["current", "optimal", "delta", "performance_score"]
        },
        {
            "name": "Vehicles List",
            "url": f"{BASE_URL}/vehicles",
            "keys": ["vehicles"]
        },
        {
            "name": "Tire Degradation",
            "url": f"{BASE_URL}/tire-degradation/78",
            "keys": ["vehicle_number", "total_laps", "best_lap_time", "laps"]
        },
        {
            "name": "Track Geometry",
            "url": f"{BASE_URL}/api/tracks/barber/geometry",
            "keys": ["points", "track_name", "length_km", "turns"]
        },
        {
            "name": "AI Query",
            "url": f"{BASE_URL}/ai/query",
            "keys": ["response", "type", "confidence"],
            "method": "POST",
            "data": {
                "query": "Tell me about Barber Motorsports Park",
                "context": {"track": "barber", "lap": 15}
            }
        }
    ]
    
    results = []
    for test in tests:
        if test.get("method") == "POST":
            # POST request
            try:
                response = requests.post(test["url"], json=test["data"], timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"\n{'='*60}")
                    print(f"Testing: {test['name']}")
                    print(f"URL: {test['url']}")
                    print('-'*60)
                    print(f"✅ SUCCESS - Status: {response.status_code}")
                    print(f"Response: {data.get('response', '')[:100]}...")
                    results.append(True)
                else:
                    print(f"❌ FAILED - Status: {response.status_code}")
                    results.append(False)
            except Exception as e:
                print(f"❌ ERROR: {e}")
                results.append(False)
        else:
            # GET request
            success = test_endpoint(test["name"], test["url"], test["keys"])
            results.append(success)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Real data integration is working!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
    
    print("="*60)


if __name__ == "__main__":
    main()
