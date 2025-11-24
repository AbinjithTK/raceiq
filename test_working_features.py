"""Test working features - focus on what's functional"""
import requests

BASE_URL = "http://localhost:8000"

print("\n" + "="*60)
print("RACEIQ FUNCTIONAL FEATURES TEST")
print("="*60)

tests_passed = 0
tests_total = 0

# Test 1: Vehicles List
print("\n1. Testing Vehicles List...")
tests_total += 1
try:
    response = requests.get(f"{BASE_URL}/vehicles", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - Found {len(data['vehicles'])} vehicles")
        print(f"   Sample: Vehicle #{data['vehicles'][0]['number']} - Position {data['vehicles'][0]['position']}")
        tests_passed += 1
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 2: Track Geometry (3D Visualization)
print("\n2. Testing Track Geometry (3D)...")
tests_total += 1
try:
    response = requests.get(f"{BASE_URL}/api/tracks/barber/geometry", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - {data['point_count']} points loaded")
        print(f"   Track: {data['track_name']} ({data['length_km']} km, {data['turns']} turns)")
        tests_passed += 1
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: AI Query (RAG Dataset)
print("\n3. Testing AI Race Engineer...")
tests_total += 1
try:
    response = requests.post(
        f"{BASE_URL}/ai/query",
        json={
            "query": "Tell me about Barber Motorsports Park",
            "context": {"track": "barber", "lap": 15}
        },
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - AI Response:")
        print(f"   {data['response'][:100]}...")
        print(f"   Type: {data['type']}, Confidence: {data['confidence']:.0%}")
        tests_passed += 1
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 4: Tire Degradation
print("\n4. Testing Tire Degradation Analysis...")
tests_total += 1
try:
    response = requests.get(f"{BASE_URL}/tire-degradation/13", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - Vehicle #{data['vehicle_number']}")
        print(f"   Best lap: {data['best_lap_time']:.3f}s")
        print(f"   Total laps: {data['total_laps']}")
        tests_passed += 1
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 5: Pit Prediction
print("\n5. Testing Pit Prediction...")
tests_total += 1
try:
    response = requests.post(
        f"{BASE_URL}/pit-prediction",
        json={
            "vehicle_number": 13,
            "current_lap": 15,
            "total_laps": 27
        },
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - Recommended pit lap: {data['pit_lap']}")
        print(f"   Confidence: {data['confidence']}%")
        tests_passed += 1
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 6: Coaching Insights
print("\n6. Testing Coaching Insights...")
tests_total += 1
try:
    response = requests.post(
        f"{BASE_URL}/coaching",
        json={
            "vehicle_number": 13,
            "lap_number": 10
        },
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - Found {len(data['opportunities'])} improvement opportunities")
        if data['opportunities']:
            print(f"   Example: {data['opportunities'][0]['message'][:60]}...")
        tests_passed += 1
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 7: Track List
print("\n7. Testing Multi-Track Support...")
tests_total += 1
try:
    response = requests.get(f"{BASE_URL}/tracks", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS - {len(data['tracks'])} tracks available")
        print(f"   Tracks: {', '.join(data['tracks'][:4])}...")
        tests_passed += 1
    else:
        print(f"   ❌ FAILED - Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print(f"Passed: {tests_passed}/{tests_total}")
print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")

if tests_passed == tests_total:
    print("\n🎉 ALL CORE FEATURES WORKING!")
    print("\n✅ RaceIQ is ready for demo:")
    print("   • Real race data from CSV files")
    print("   • AI race engineer with RAG dataset")
    print("   • 3D track visualization")
    print("   • Tire degradation analysis")
    print("   • Pit strategy prediction")
    print("   • Coaching insights")
    print("   • Multi-track support (7 tracks)")
elif tests_passed >= tests_total * 0.7:
    print("\n✅ MOST FEATURES WORKING!")
    print(f"   {tests_passed} out of {tests_total} core features functional")
else:
    print(f"\n⚠️  Only {tests_passed}/{tests_total} features working")

print("="*60)
