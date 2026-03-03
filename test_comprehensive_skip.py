import requests
import json
from datetime import date

base_url = "http://localhost:8080/api/v1"
headers = {"Content-Type": "application/json"}

def get_test_data():
    print("Fetching test data...")
    try:
        # Get a bus
        res = requests.get(f"{base_url}/buses", headers=headers)
        buses = res.json()
        if not buses: return None
        bus = buses[0]
        
        # Get a driver
        res = requests.get(f"{base_url}/drivers", headers=headers)
        drivers = res.json()
        if not drivers: return None
        driver = drivers[0]
        
        # Get a route
        res = requests.get(f"{base_url}/routes", headers=headers)
        routes = res.json()
        if not routes: return None
        route = routes[0]
        
        return {
            "bus_id": bus['bus_id'],
            "driver_id": driver['driver_id'],
            "route_id": route['route_id']
        }
    except Exception as e:
        print(f"Error fetching test data: {e}")
        return None

def run_tests():
    data = get_test_data()
    if not data:
        print("Could not find enough data to run tests.")
        return

    print(f"Using Data: {data}")

    # 1. Create Trip
    print("\n1. Creating test trip...")
    trip_payload = {
        "bus_id": data['bus_id'],
        "driver_id": data['driver_id'],
        "route_id": data['route_id'],
        "trip_date": str(date.today()),
        "trip_type": "PICKUP"
    }
    res = requests.post(f"{base_url}/trips", json=trip_payload, headers=headers)
    if res.status_code != 200:
        print(f"Failed to create trip: {res.text}")
        return
    trip = res.json()
    trip_id = trip['trip_id']
    print(f"Created Trip: {trip_id}")

    # 2. Start Trip
    print("\n2. Starting trip...")
    res = requests.put(f"{base_url}/trips/{trip_id}/status", json={"status": "ONGOING"}, headers=headers)
    print(f"Start Status: {res.status_code}")

    # 3. Test Skip Next Stop (Skip Stop 1)
    print("\n3. Testing Skip Next Stop (Stop 1)...")
    res = requests.post(f"{base_url}/trips/{trip_id}/skip-next-stop", headers=headers)
    print(f"Skip Next Status: {res.status_code}")
    print(f"Response: {res.json()}")

    # 4. Test Skip Future Stop (Skip Stop 5)
    print("\n4. Testing Skip Future Stop (Stop 5)...")
    res = requests.post(f"{base_url}/trips/{trip_id}/skip-future-stop/5", headers=headers)
    print(f"Skip Future Status: {res.status_code}")
    print(f"Response: {res.json()}")

    # 5. Check Trip Progress
    print("\n5. Checking trip state...")
    res = requests.get(f"{base_url}/trips/{trip_id}", headers=headers)
    final_trip = res.json()
    print(f"Current Stop Order: {final_trip.get('current_stop_order')}")
    print(f"Skipped Stops JSON: {final_trip.get('skipped_stops')}")

    # 6. Cleanup (Optional)
    # print("\n6. Deleting test trip...")
    # requests.delete(f"{base_url}/trips/{trip_id}", headers=headers)

if __name__ == "__main__":
    run_tests()
