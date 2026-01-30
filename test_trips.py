
import requests
import json
import uuid
from datetime import date, datetime

BASE_URL = "http://localhost:8000"

def print_result(name, success, data=None):
    if success:
        print(f"✅ {name}: PASSED")
    else:
        print(f"❌ {name}: FAILED")
        if data:
            print(f"   Error: {data}")

def main():
    print("🚀 Starting Trip Management API Tests...")

    # 1. Login as Admin
    print("\n🔐 Authenticating...")
    # First ensure we have an admin
    admin_phone = "9998887776"
    admin_password = "password123"
    
    # Try login first
    login_data = {
        "phone": admin_phone,
        "password": admin_password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code != 200:
        print("   Admin not found, creating one...")
        admin_data = {
            "name": "Test Admin",
            "phone": admin_phone,
            "email": "testadmin@example.com",
            "password": admin_password
        }
        res = requests.post(f"{BASE_URL}/admins", json=admin_data)
        if res.status_code != 201 and res.status_code != 400: # 400 means already exists which contradicts login fail, but handle safely
             print(f"Failed to create admin: {res.text}")
             return
        
        # Login again
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Authentication successful!")

    # 2. Setup Prerequisites (Route, Driver, Bus, Stops)
    print("\n🛠 Setting up prerequisites...")
    
    # Create Route
    print("   Creating Route...")
    route_data = {"name": f"Test Route {uuid.uuid4().hex[:6]}"}
    res = requests.post(f"{BASE_URL}/routes", json=route_data, headers=headers)
    if res.status_code != 201:
        print(f"Failed to create route: {res.text}")
        return
    route_id = res.json()["route_id"]
    print_result("Create Route", True)

    # Create Route Stops
    print("   Creating Route Stops...")
    stop1_data = {
        "route_id": route_id,
        "stop_name": "Stop 1",
        "latitude": 12.0,
        "longitude": 77.0,
        "stop_order": 1
    }
    res = requests.post(f"{BASE_URL}/route-stops", json=stop1_data, headers=headers)
    stop1_id = res.json()["stop_id"] if res.status_code == 201 else None

    stop2_data = {
        "route_id": route_id,
        "stop_name": "Stop 2",
        "latitude": 12.1,
        "longitude": 77.1,
        "stop_order": 2
    }
    res = requests.post(f"{BASE_URL}/route-stops", json=stop2_data, headers=headers)
    stop2_id = res.json()["stop_id"] if res.status_code == 201 else None
    
    if not stop1_id or not stop2_id:
        print("Failed to create stops")
        return
    print_result("Create Stops", True)

    # Create Driver
    print("   Creating Driver...")
    driver_phone = f"{uuid.uuid4().int}"[:10]
    driver_data = {
        "name": "Test Driver",
        "phone": driver_phone,
        "email": f"driver{uuid.uuid4().hex[:6]}@test.com",
        "password": "password",
        "dob": "1990-01-01",
        "licence_number": f"LIC{uuid.uuid4().hex[:6]}",
        "licence_expiry": "2030-01-01",
        "aadhar_number": f"1234{uuid.uuid4().int}"[:12],
        "licence_url": "http://example.com/licence.jpg",
        "aadhar_url": "http://example.com/aadhar.jpg",
        "photo_url": "http://example.com/photo.jpg",
        "fcm_token": "test_token"
    }
    # Note: The API might expect different fields based on the report ("kyc_verified" issue), but let's try with standard fields from models (guessed) or what we saw in routes.py
    # routes.py create_driver expects DriverCreate. Let's see models.py if needed, but routes.py lines 449-454 list the fields.
    
    res = requests.post(f"{BASE_URL}/drivers", json=driver_data, headers=headers)
    if res.status_code != 201:
        print(f"Failed to create driver: {res.text}")
        return
    driver_id = res.json()["driver_id"]
    print_result("Create Driver", True)

    # Create Bus
    print("   Creating Bus...")
    bus_number = f"KA01{uuid.uuid4().hex[:4].upper()}"
    bus_data = {
        "bus_number": bus_number,
        "driver_id": driver_id,
        "route_id": route_id,
        "bus_type": "SCHOOL_BUS",
        "bus_brand": "Tata",
        "bus_model": "Starbus",
        "seating_capacity": 40,
        "rc_expiry_date": "2030-01-01",
        "fc_expiry_date": "2030-01-01",
        "rc_book_url": "http://example.com/rc.jpg",
        "fc_certificate_url": "http://example.com/fc.jpg",
        "bus_front_url": "http://example.com/front.jpg",
        "bus_back_url": "http://example.com/back.jpg",
        "bus_left_url": "http://example.com/left.jpg",
        "bus_right_url": "http://example.com/right.jpg"
    }
    res = requests.post(f"{BASE_URL}/buses", json=bus_data, headers=headers)
    if res.status_code != 201:
        print(f"Failed to create bus: {res.text}")
        return
    bus_id = res.json()["bus_id"]
    print_result("Create Bus", True)

    # 3. Test Trip Endpoints
    print("\n🚌 Testing Trip Endpoints...")

    # 3.1 Create Trip
    print("\n1. Testing POST /trips")
    trip_data = {
        "bus_id": bus_id,
        "driver_id": driver_id,
        "route_id": route_id,
        "trip_date": date.today().isoformat(),
        "trip_type": "PICKUP"
    }
    res = requests.post(f"{BASE_URL}/trips", json=trip_data, headers=headers)
    print_result("Create Trip", res.status_code == 201, res.text)
    if res.status_code != 201: return
    trip_id = res.json()["trip_id"]

    # 3.2 Get All Trips
    print("\n2. Testing GET /trips")
    res = requests.get(f"{BASE_URL}/trips", headers=headers)
    print_result("Get All Trips", res.status_code == 200, res.text)

    # 3.3 Get Trip by ID
    print("\n3. Testing GET /trips/{trip_id}")
    res = requests.get(f"{BASE_URL}/trips/{trip_id}", headers=headers)
    print_result("Get Trip by ID", res.status_code == 200, res.text)

    # 3.4 Update Trip
    print("\n4. Testing PUT /trips/{trip_id}")
    update_data = {"trip_type": "DROP"}
    res = requests.put(f"{BASE_URL}/trips/{trip_id}", json=update_data, headers=headers)
    print_result("Update Trip", res.status_code == 200, res.text)

    # 3.5 Start Trip
    print("\n5. Testing POST /trips/{trip_id}/start")
    res = requests.post(f"{BASE_URL}/trips/{trip_id}/start", headers=headers)
    print_result("Start Trip", res.status_code == 200, res.text)

    # 3.6 Get Trip Status
    print("\n6. Testing GET /trips/{trip_id}/status")
    res = requests.get(f"{BASE_URL}/trips/{trip_id}/status", headers=headers)
    print_result("Get Trip Status", res.status_code == 200, res.text)

    # 3.6 Get Next Stop Info (This is a GET request, not the action to move)
    print("\n6b. Testing GET /trips/{trip_id}/next-stop (Info)")
    res = requests.get(f"{BASE_URL}/trips/{trip_id}/next-stop", headers=headers)
    print_result("Get Next Stop Info", res.status_code == 200, res.text)

    # 3.7 Move to Next Stop
    print("\n7. Testing POST /trips/{trip_id}/next-stop")
    res = requests.post(f"{BASE_URL}/trips/{trip_id}/next-stop", headers=headers)
    print_result("Move to Next Stop", res.status_code == 200, res.text)

    # 3.8 Get Current Stop Students
    # Note: We didn't add students, so this might return empty list or fail depending on logic, but checking status 200
    print("\n8. Testing GET /trips/{trip_id}/current-stop-students")
    res = requests.get(f"{BASE_URL}/trips/{trip_id}/current-stop-students", headers=headers)
    print_result("Get Current Stop Students", res.status_code == 200, res.text)

    # 3.9 Pickup Schedule
    print("\n9. Testing GET /trips/pickup-schedule")
    res = requests.get(f"{BASE_URL}/trips/pickup-schedule", headers=headers)
    print_result("Get Pickup Schedule", res.status_code == 200, res.text)

    # 3.10 Drop Schedule
    print("\n10. Testing GET /trips/drop-schedule")
    res = requests.get(f"{BASE_URL}/trips/drop-schedule", headers=headers)
    print_result("Get Drop Schedule", res.status_code == 200, res.text)

    # 3.11 Delete Trip
    print("\n11. Testing DELETE /trips/{trip_id}")
    res = requests.delete(f"{BASE_URL}/trips/{trip_id}", headers=headers)
    print_result("Delete Trip", res.status_code == 204, res.text)

if __name__ == "__main__":
    main()
