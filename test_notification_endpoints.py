import requests
import json

base_url = "http://localhost:8080/api/v1"
headers = {"Content-Type": "application/json"}

# 1. Test bus-tracking/stop-progression
print("Testing /bus-tracking/stop-progression...")
try:
    res = requests.post(f"{base_url}/bus-tracking/stop-progression", json={"trip_id": "dummy", "latitude": 0.0, "longitude": 0.0}, headers=headers)
    print("Status:", res.status_code)
    print("Response:", res.json())
except Exception as e:
    print("Error:", e)

# 2. Test bus-tracking/location
print("\nTesting /bus-tracking/location...")
try:
    res = requests.post(f"{base_url}/bus-tracking/location", json={"trip_id": "dummy", "latitude": 0.0, "longitude": 0.0}, headers=headers)
    print("Status:", res.status_code)
    print("Response:", res.json())
except Exception as e:
    print("Error:", e)
    
# 3. Test bus-tracking/notify (Custom Notification)
print("\nTesting /bus-tracking/notify...")
try:
    res = requests.post(f"{base_url}/bus-tracking/notify", json={"trip_id": "dummy", "message": "Test"}, headers=headers)
    print("Status:", res.status_code)
    print("Response:", res.json())
except Exception as e:
    print("Error:", e)
    
# 4. Test start trip (requires auth / trip id)
print("\nTesting /trip/start...")
headers_auth = {"Content-Type": "application/json", "x-admin-key": "admin_secret"}
try:
    # Not guessing the admin key, just testing if it fails with unauthorized or 404
    res = requests.post(f"{base_url}/trip/start?trip_id=dummy", headers=headers_auth)
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except:
        print("Response Text:", res.text)
except Exception as e:
    print("Error:", e)
