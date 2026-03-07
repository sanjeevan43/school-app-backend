import requests
import json
import uuid

BASE_URL = "http://localhost:8080/api/v1"
ADMIN_KEY = "selvagam-admin-key-2024"
HEADERS = {"x-admin-key": ADMIN_KEY}

def test_new_json_format():
    # 1. Get real data
    try:
        buses = requests.get(f"{BASE_URL}/buses", headers=HEADERS).json()
        driver = requests.get(f"{BASE_URL}/drivers", headers=HEADERS).json()
        routes = requests.get(f"{BASE_URL}/routes", headers=HEADERS).json()
        
        if not (buses and driver and routes):
            print("Missing test data")
            return
            
        bus_id = buses[0]['bus_id']
        driver_id = driver[0]['driver_id']
        route_id = routes[0]['route_id']
        
        # 2. Create a trip
        trip_payload = {
            "bus_id": bus_id,
            "driver_id": driver_id,
            "route_id": route_id,
            "trip_date": "2026-03-07",
            "trip_type": "PICKUP"
        }
        
        create_res = requests.post(f"{BASE_URL}/trips", json=trip_payload, headers=HEADERS)
        print(f"Create Trip Status: {create_res.status_code}")
        trip = create_res.json()
        trip_id = trip['trip_id']
        
        # 3. Start Trip (Check initialization)
        start_res = requests.put(f"{BASE_URL}/trips/{trip_id}/start", headers=HEADERS)
        print(f"Start Trip Status: {start_res.status_code}")
        
        trip_data = requests.get(f"{BASE_URL}/trips/{trip_id}", headers=HEADERS).json()
        print(f"Initial stop_logs: {json.dumps(trip_data.get('stop_logs'), indent=2)}")
        
        # 4. Simulate arrival at stop 1
        # Need stop coords
        stops = requests.get(f"{BASE_URL}/route-stops", params={"route_id": route_id}, headers=HEADERS).json()
        if stops:
            stop = stops[0]
            track_payload = {
                "trip_id": trip_id,
                "latitude": stop['latitude'],
                "longitude": stop['longitude']
            }
            track_res = requests.post(f"{BASE_URL}/bus-tracking/stop-progression", json=track_payload, headers=HEADERS)
            print(f"Tracking Status: {track_res.status_code}")
            
            # 5. Check logs again
            trip_data = requests.get(f"{BASE_URL}/trips/{trip_id}", headers=HEADERS).json()
            print(f"Logs after arrival: {json.dumps(trip_data.get('stop_logs'), indent=2)}")
            
            # 6. Skip next stop
            skip_res = requests.post(f"{BASE_URL}/trips/{trip_id}/skip-next-stop", headers=HEADERS)
            print(f"Skip Status: {skip_res.status_code}")
            
            trip_data = requests.get(f"{BASE_URL}/trips/{trip_id}", headers=HEADERS).json()
            print(f"Logs after skip: {json.dumps(trip_data.get('stop_logs'), indent=2)}")

    except Exception as e:
        print(f"Test Exception: {e}")

if __name__ == "__main__":
    test_new_json_format()
