#!/usr/bin/env python3
"""
Comprehensive API Test Script
Tests all endpoints in the School Transport Management API
"""

import requests
import json
import uuid
from datetime import date, datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_api_endpoints():
    print("🚀 Testing School Transport Management API")
    print("=" * 50)
    
    # Test data
    admin_token = None
    admin_id = None
    parent_id = None
    driver_id = None
    route_id = None
    bus_id = None
    stop_id = None
    student_id = None
    trip_id = None
    
    # 1. Test Encryption/Decryption
    print("\n1️⃣ Testing Encryption/Decryption...")
    try:
        # Test encryption
        encrypt_response = requests.post(f"{BASE_URL}/encrypt", json={"text": "Hello World"})
        if encrypt_response.status_code == 200:
            print("✅ Encryption works")
            encrypted_text = encrypt_response.json()["encrypted_text"]
            
            # Test decryption
            decrypt_response = requests.post(f"{BASE_URL}/decrypt", json={"encrypted_text": encrypted_text})
            if decrypt_response.status_code == 200:
                print("✅ Decryption works")
            else:
                print(f"❌ Decryption failed: {decrypt_response.status_code}")
        else:
            print(f"❌ Encryption failed: {encrypt_response.status_code}")
    except Exception as e:
        print(f"❌ Encryption/Decryption error: {e}")
    
    # 2. Test Admin Creation
    print("\n2️⃣ Testing Admin Management...")
    try:
        admin_data = {
            "phone": 9876543210,
            "email": "admin@school.com",
            "name": "Test Admin",
            "password": "admin123",
            "dob": "1990-01-01"
        }
        
        response = requests.post(f"{BASE_URL}/admins", json=admin_data)
        if response.status_code == 201:
            print("✅ Admin created successfully")
            admin = response.json()
            admin_id = admin["admin_id"]
        elif response.status_code == 400 and "already registered" in response.text:
            print("⚠️ Admin already exists")
            # Get existing admin
            response = requests.get(f"{BASE_URL}/admins")
            if response.status_code == 200:
                admins = response.json()
                if admins:
                    admin_id = admins[0]["admin_id"]
        else:
            print(f"❌ Admin creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Admin creation error: {e}")
    
    # 3. Test Admin Login
    print("\n3️⃣ Testing Authentication...")
    try:
        login_data = {
            "phone": 9876543210,
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Admin login successful")
            token_data = response.json()
            admin_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {admin_token}"}
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            headers = {}
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        headers = {}
    
    # 4. Test Admin Profile
    try:
        response = requests.get(f"{BASE_URL}/admins/profile", headers=headers)
        if response.status_code == 200:
            print("✅ Admin profile retrieved")
        else:
            print(f"❌ Admin profile failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Admin profile error: {e}")
    
    # 5. Test Parent Management
    print("\n4️⃣ Testing Parent Management...")
    try:
        parent_data = {
            "phone": 9123456789,
            "email": "parent@test.com",
            "name": "Test Parent",
            "password": "parent123",
            "dob": "1985-05-15",
            "parent_role": "MOTHER",
            "city": "Mumbai"
        }
        
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        if response.status_code == 201:
            print("✅ Parent created successfully")
            parent = response.json()
            parent_id = parent["parent_id"]
        else:
            print(f"❌ Parent creation failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Parent creation error: {e}")
    
    # Test get all parents
    try:
        response = requests.get(f"{BASE_URL}/parents", headers=headers)
        if response.status_code == 200:
            print("✅ Get all parents works")
        else:
            print(f"❌ Get all parents failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all parents error: {e}")
    
    # 6. Test Driver Management
    print("\n5️⃣ Testing Driver Management...")
    try:
        driver_data = {
            "name": "Test Driver",
            "phone": 9987654321,
            "email": "driver@test.com",
            "password": "driver123",
            "dob": "1980-03-20",
            "licence_number": "DL123456789",
            "licence_expiry": "2025-12-31",
            "aadhar_number": "123456789012"
        }
        
        response = requests.post(f"{BASE_URL}/drivers", json=driver_data, headers=headers)
        if response.status_code == 201:
            print("✅ Driver created successfully")
            driver = response.json()
            driver_id = driver["driver_id"]
        else:
            print(f"❌ Driver creation failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Driver creation error: {e}")
    
    # Test get all drivers
    try:
        response = requests.get(f"{BASE_URL}/drivers", headers=headers)
        if response.status_code == 200:
            print("✅ Get all drivers works")
        else:
            print(f"❌ Get all drivers failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all drivers error: {e}")
    
    # 7. Test Route Management
    print("\n6️⃣ Testing Route Management...")
    try:
        route_data = {
            "name": "Route A - Main Street"
        }
        
        response = requests.post(f"{BASE_URL}/routes", json=route_data, headers=headers)
        if response.status_code == 201:
            print("✅ Route created successfully")
            route = response.json()
            route_id = route["route_id"]
        else:
            print(f"❌ Route creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Route creation error: {e}")
    
    # Test get all routes
    try:
        response = requests.get(f"{BASE_URL}/routes", headers=headers)
        if response.status_code == 200:
            print("✅ Get all routes works")
        else:
            print(f"❌ Get all routes failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all routes error: {e}")
    
    # 8. Test Bus Management
    print("\n7️⃣ Testing Bus Management...")
    if driver_id and route_id:
        try:
            bus_data = {
                "bus_number": "MH01AB1234",
                "driver_id": driver_id,
                "route_id": route_id,
                "bus_type": "AC",
                "bus_brand": "Tata",
                "bus_model": "Starbus",
                "seating_capacity": 40,
                "rc_expiry_date": "2025-12-31",
                "fc_expiry_date": "2024-12-31"
            }
            
            response = requests.post(f"{BASE_URL}/buses", json=bus_data, headers=headers)
            if response.status_code == 201:
                print("✅ Bus created successfully")
                bus = response.json()
                bus_id = bus["bus_id"]
            else:
                print(f"❌ Bus creation failed: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Bus creation error: {e}")
    else:
        print("⚠️ Skipping bus creation - missing driver or route")
    
    # Test get all buses
    try:
        response = requests.get(f"{BASE_URL}/buses", headers=headers)
        if response.status_code == 200:
            print("✅ Get all buses works")
        else:
            print(f"❌ Get all buses failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all buses error: {e}")
    
    # 9. Test Route Stops Management
    print("\n8️⃣ Testing Route Stops Management...")
    if route_id:
        try:
            stop_data = {
                "route_id": route_id,
                "stop_name": "Main Gate",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "stop_order": 1
            }
            
            response = requests.post(f"{BASE_URL}/route-stops", json=stop_data, headers=headers)
            if response.status_code == 201:
                print("✅ Route stop created successfully")
                stop = response.json()
                stop_id = stop["stop_id"]
            else:
                print(f"❌ Route stop creation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Route stop creation error: {e}")
    else:
        print("⚠️ Skipping route stop creation - missing route")
    
    # Test get all route stops
    try:
        response = requests.get(f"{BASE_URL}/route-stops", headers=headers)
        if response.status_code == 200:
            print("✅ Get all route stops works")
        else:
            print(f"❌ Get all route stops failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all route stops error: {e}")
    
    # 10. Test Student Management
    print("\n9️⃣ Testing Student Management...")
    if parent_id and route_id and stop_id:
        try:
            student_data = {
                "parent_id": parent_id,
                "name": "Test Student",
                "dob": "2010-08-15",
                "class_section": "5A",
                "route_id": route_id,
                "pickup_stop_id": stop_id,
                "drop_stop_id": stop_id
            }
            
            response = requests.post(f"{BASE_URL}/students", json=student_data, headers=headers)
            if response.status_code == 201:
                print("✅ Student created successfully")
                student = response.json()
                student_id = student["student_id"]
            else:
                print(f"❌ Student creation failed: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Student creation error: {e}")
    else:
        print("⚠️ Skipping student creation - missing parent, route, or stop")
    
    # Test get all students
    try:
        response = requests.get(f"{BASE_URL}/students", headers=headers)
        if response.status_code == 200:
            print("✅ Get all students works")
        else:
            print(f"❌ Get all students failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all students error: {e}")
    
    # 11. Test Trip Management
    print("\n🔟 Testing Trip Management...")
    if bus_id and driver_id and route_id:
        try:
            trip_data = {
                "bus_id": bus_id,
                "driver_id": driver_id,
                "route_id": route_id,
                "trip_date": str(date.today()),
                "trip_type": "PICKUP"
            }
            
            response = requests.post(f"{BASE_URL}/trips", json=trip_data, headers=headers)
            if response.status_code == 201:
                print("✅ Trip created successfully")
                trip = response.json()
                trip_id = trip["trip_id"]
            else:
                print(f"❌ Trip creation failed: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Trip creation error: {e}")
    else:
        print("⚠️ Skipping trip creation - missing bus, driver, or route")
    
    # Test get all trips
    try:
        response = requests.get(f"{BASE_URL}/trips", headers=headers)
        if response.status_code == 200:
            print("✅ Get all trips works")
        else:
            print(f"❌ Get all trips failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get all trips error: {e}")
    
    # 12. Test FCM Token Updates
    print("\n1️⃣1️⃣ Testing FCM Token Updates...")
    if parent_id:
        try:
            fcm_data = {"fcm_token": "test_fcm_token_parent"}
            response = requests.put(f"{BASE_URL}/parents/{parent_id}/fcm-token", json=fcm_data, headers=headers)
            if response.status_code == 200:
                print("✅ Parent FCM token update works")
            else:
                print(f"❌ Parent FCM token update failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Parent FCM token update error: {e}")
    
    if driver_id:
        try:
            fcm_data = {"fcm_token": "test_fcm_token_driver"}
            response = requests.put(f"{BASE_URL}/drivers/{driver_id}/fcm-token", json=fcm_data, headers=headers)
            if response.status_code == 200:
                print("✅ Driver FCM token update works")
            else:
                print(f"❌ Driver FCM token update failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Driver FCM token update error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("Check the results above for any failed endpoints.")
    print("Visit http://localhost:8000/docs for interactive API documentation.")

if __name__ == "__main__":
    test_api_endpoints()