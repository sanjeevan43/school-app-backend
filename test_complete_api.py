#!/usr/bin/env python3
"""
Complete API Test Script with Database Connection
Tests all endpoints in the School Transport Management API
"""

import requests
import json
import uuid
from datetime import date, datetime
import time

BASE_URL = "http://localhost:8080/api/v1"

def print_test_result(test_name, success, message=""):
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")

def test_database_connection():
    """Test database connection via health endpoint"""
    print("\n🔍 Testing Database Connection...")
    try:
        response = requests.get("http://localhost:8080/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("database") == "connected":
                print_test_result("Database Connection", True, "Database is connected")
                return True
            else:
                print_test_result("Database Connection", False, "Database not connected")
                return False
        else:
            print_test_result("Database Connection", False, f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Database Connection", False, f"Connection error: {e}")
        return False

def test_encryption_endpoints():
    """Test encryption/decryption endpoints"""
    print("\n🔐 Testing Encryption/Decryption...")
    
    try:
        # Test encryption
        encrypt_data = {"text": "Hello World Test"}
        response = requests.post(f"{BASE_URL}/encrypt", json=encrypt_data)
        
        if response.status_code == 200:
            encrypted_text = response.json()["encrypted_text"]
            print_test_result("Text Encryption", True, f"Encrypted: {encrypted_text[:20]}...")
            
            # Test decryption
            decrypt_data = {"encrypted_text": encrypted_text}
            response = requests.post(f"{BASE_URL}/decrypt", json=decrypt_data)
            
            if response.status_code == 200:
                decrypted_text = response.json()["decrypted_text"]
                success = decrypted_text == "Hello World Test"
                print_test_result("Text Decryption", success, f"Decrypted: {decrypted_text}")
                return success
            else:
                print_test_result("Text Decryption", False, f"Status: {response.status_code}")
                return False
        else:
            print_test_result("Text Encryption", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Encryption/Decryption", False, f"Error: {e}")
        return False

def test_admin_management():
    """Test admin CRUD operations"""
    print("\n👨‍💼 Testing Admin Management...")
    
    admin_data = {
        "phone": 9876543210,
        "email": "admin@test.com",
        "name": "Test Admin",
        "password": "admin123",
        "dob": "1990-01-01"
    }
    
    try:
        # Create admin
        response = requests.post(f"{BASE_URL}/admins", json=admin_data)
        
        if response.status_code == 201:
            admin = response.json()
            admin_id = admin["admin_id"]
            print_test_result("Create Admin", True, f"Admin ID: {admin_id}")
        elif response.status_code == 400 and "already registered" in response.text:
            print_test_result("Create Admin", True, "Admin already exists")
            # Get existing admin
            response = requests.get(f"{BASE_URL}/admins")
            if response.status_code == 200:
                admins = response.json()
                admin_id = admins[0]["admin_id"] if admins else None
            else:
                admin_id = None
        else:
            print_test_result("Create Admin", False, f"Status: {response.status_code}")
            return None, None
        
        # Test admin login
        login_data = {"phone": 9876543210, "password": "admin123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            print_test_result("Admin Login", True, "Token received")
        else:
            print_test_result("Admin Login", False, f"Status: {response.status_code}")
            return None, None
        
        # Test get admin profile
        response = requests.get(f"{BASE_URL}/admins/profile", headers=headers)
        print_test_result("Get Admin Profile", response.status_code == 200)
        
        # Test get all admins
        response = requests.get(f"{BASE_URL}/admins", headers=headers)
        print_test_result("Get All Admins", response.status_code == 200)
        
        return admin_id, headers
        
    except Exception as e:
        print_test_result("Admin Management", False, f"Error: {e}")
        return None, None

def test_parent_management(headers):
    """Test parent CRUD operations"""
    print("\n👨‍👩‍👧‍👦 Testing Parent Management...")
    
    parent_data = {
        "phone": 9123456789,
        "email": "parent@test.com",
        "name": "Test Parent",
        "password": "parent123",
        "dob": "1985-05-15",
        "parent_role": "MOTHER",
        "city": "Mumbai"
    }
    
    try:
        # Create parent
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        
        if response.status_code == 201:
            parent = response.json()
            parent_id = parent["parent_id"]
            print_test_result("Create Parent", True, f"Parent ID: {parent_id}")
        else:
            print_test_result("Create Parent", False, f"Status: {response.status_code}, Response: {response.text}")
            return None
        
        # Test parent login
        login_data = {"phone": 9123456789, "password": "parent123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_test_result("Parent Login", response.status_code == 200)
        
        # Test get all parents
        response = requests.get(f"{BASE_URL}/parents", headers=headers)
        print_test_result("Get All Parents", response.status_code == 200)
        
        # Test get parent by ID
        response = requests.get(f"{BASE_URL}/parents/{parent_id}", headers=headers)
        print_test_result("Get Parent by ID", response.status_code == 200)
        
        # Test update parent
        update_data = {"city": "Delhi"}
        response = requests.put(f"{BASE_URL}/parents/{parent_id}", json=update_data, headers=headers)
        print_test_result("Update Parent", response.status_code == 200)
        
        return parent_id
        
    except Exception as e:
        print_test_result("Parent Management", False, f"Error: {e}")
        return None

def test_driver_management(headers):
    """Test driver CRUD operations"""
    print("\n🚗 Testing Driver Management...")
    
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
    
    try:
        # Create driver
        response = requests.post(f"{BASE_URL}/drivers", json=driver_data, headers=headers)
        
        if response.status_code == 201:
            driver = response.json()
            driver_id = driver["driver_id"]
            print_test_result("Create Driver", True, f"Driver ID: {driver_id}")
        else:
            print_test_result("Create Driver", False, f"Status: {response.status_code}, Response: {response.text}")
            return None
        
        # Test driver login
        login_data = {"phone": 9987654321, "password": "driver123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_test_result("Driver Login", response.status_code == 200)
        
        # Test get all drivers
        response = requests.get(f"{BASE_URL}/drivers", headers=headers)
        print_test_result("Get All Drivers", response.status_code == 200)
        
        # Test get available drivers
        response = requests.get(f"{BASE_URL}/drivers/available", headers=headers)
        print_test_result("Get Available Drivers", response.status_code == 200)
        
        return driver_id
        
    except Exception as e:
        print_test_result("Driver Management", False, f"Error: {e}")
        return None

def test_route_management(headers):
    """Test route CRUD operations"""
    print("\n🛣️ Testing Route Management...")
    
    route_data = {"name": "Route A - Main Street"}
    
    try:
        # Create route
        response = requests.post(f"{BASE_URL}/routes", json=route_data, headers=headers)
        
        if response.status_code == 201:
            route = response.json()
            route_id = route["route_id"]
            print_test_result("Create Route", True, f"Route ID: {route_id}")
        else:
            print_test_result("Create Route", False, f"Status: {response.status_code}")
            return None
        
        # Test get all routes
        response = requests.get(f"{BASE_URL}/routes", headers=headers)
        print_test_result("Get All Routes", response.status_code == 200)
        
        # Test get route by ID
        response = requests.get(f"{BASE_URL}/routes/{route_id}", headers=headers)
        print_test_result("Get Route by ID", response.status_code == 200)
        
        return route_id
        
    except Exception as e:
        print_test_result("Route Management", False, f"Error: {e}")
        return None

def test_bus_management(headers, driver_id, route_id):
    """Test bus CRUD operations"""
    print("\n🚌 Testing Bus Management...")
    
    if not driver_id or not route_id:
        print_test_result("Bus Management", False, "Missing driver or route ID")
        return None
    
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
    
    try:
        # Create bus
        response = requests.post(f"{BASE_URL}/buses", json=bus_data, headers=headers)
        
        if response.status_code == 201:
            bus = response.json()
            bus_id = bus["bus_id"]
            print_test_result("Create Bus", True, f"Bus ID: {bus_id}")
        else:
            print_test_result("Create Bus", False, f"Status: {response.status_code}, Response: {response.text}")
            return None
        
        # Test get all buses
        response = requests.get(f"{BASE_URL}/buses", headers=headers)
        print_test_result("Get All Buses", response.status_code == 200)
        
        # Test get bus by ID
        response = requests.get(f"{BASE_URL}/buses/{bus_id}", headers=headers)
        print_test_result("Get Bus by ID", response.status_code == 200)
        
        return bus_id
        
    except Exception as e:
        print_test_result("Bus Management", False, f"Error: {e}")
        return None

def test_route_stops_management(headers, route_id):
    """Test route stops CRUD operations"""
    print("\n🚏 Testing Route Stops Management...")
    
    if not route_id:
        print_test_result("Route Stops Management", False, "Missing route ID")
        return None
    
    stop_data = {
        "route_id": route_id,
        "stop_name": "Main Gate",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "stop_order": 1
    }
    
    try:
        # Create route stop
        response = requests.post(f"{BASE_URL}/route-stops", json=stop_data, headers=headers)
        
        if response.status_code == 201:
            stop = response.json()
            stop_id = stop["stop_id"]
            print_test_result("Create Route Stop", True, f"Stop ID: {stop_id}")
        else:
            print_test_result("Create Route Stop", False, f"Status: {response.status_code}")
            return None
        
        # Test get all route stops
        response = requests.get(f"{BASE_URL}/route-stops", headers=headers)
        print_test_result("Get All Route Stops", response.status_code == 200)
        
        # Test get route stops by route
        response = requests.get(f"{BASE_URL}/route-stops?route_id={route_id}", headers=headers)
        print_test_result("Get Route Stops by Route", response.status_code == 200)
        
        return stop_id
        
    except Exception as e:
        print_test_result("Route Stops Management", False, f"Error: {e}")
        return None

def test_student_management(headers, parent_id, route_id, pickup_stop_id, drop_stop_id):
    """Test student CRUD operations"""
    print("\n👨‍🎓 Testing Student Management...")
    
    if not all([parent_id, route_id, pickup_stop_id, drop_stop_id]):
        print_test_result("Student Management", False, "Missing required IDs")
        return None
    
    student_data = {
        "parent_id": parent_id,
        "name": "Test Student",
        "dob": "2010-01-01",
        "class_section": "5A",
        "route_id": route_id,
        "pickup_stop_id": pickup_stop_id,
        "drop_stop_id": drop_stop_id
    }
    
    try:
        # Create student
        response = requests.post(f"{BASE_URL}/students", json=student_data, headers=headers)
        
        if response.status_code == 201:
            student = response.json()
            student_id = student["student_id"]
            print_test_result("Create Student", True, f"Student ID: {student_id}")
        else:
            print_test_result("Create Student", False, f"Status: {response.status_code}, Response: {response.text}")
            return None
        
        # Test get all students
        response = requests.get(f"{BASE_URL}/students", headers=headers)
        print_test_result("Get All Students", response.status_code == 200)
        
        # Test get students by parent
        response = requests.get(f"{BASE_URL}/students/parent/{parent_id}", headers=headers)
        print_test_result("Get Students by Parent", response.status_code == 200)
        
        return student_id
        
    except Exception as e:
        print_test_result("Student Management", False, f"Error: {e}")
        return None

def test_trip_management(headers, bus_id, driver_id, route_id):
    """Test trip CRUD operations"""
    print("\n🚌 Testing Trip Management...")
    
    if not all([bus_id, driver_id, route_id]):
        print_test_result("Trip Management", False, "Missing required IDs")
        return None
    
    trip_data = {
        "bus_id": bus_id,
        "driver_id": driver_id,
        "route_id": route_id,
        "trip_date": "2024-01-15",
        "trip_type": "PICKUP"
    }
    
    try:
        # Create trip
        response = requests.post(f"{BASE_URL}/trips", json=trip_data, headers=headers)
        
        if response.status_code == 201:
            trip = response.json()
            trip_id = trip["trip_id"]
            print_test_result("Create Trip", True, f"Trip ID: {trip_id}")
        else:
            print_test_result("Create Trip", False, f"Status: {response.status_code}, Response: {response.text}")
            return None
        
        # Test get all trips
        response = requests.get(f"{BASE_URL}/trips", headers=headers)
        print_test_result("Get All Trips", response.status_code == 200)
        
        # Test get trips by route
        response = requests.get(f"{BASE_URL}/trips?route_id={route_id}", headers=headers)
        print_test_result("Get Trips by Route", response.status_code == 200)
        
        return trip_id
        
    except Exception as e:
        print_test_result("Trip Management", False, f"Error: {e}")
        return None

def main():
    """Main test function"""
    print("🚀 School Transport Management API - Complete Test Suite")
    print("=" * 60)
    
    # Test database connection first
    if not test_database_connection():
        print("\n❌ Database connection failed. Please check your database configuration.")
        return
    
    # Test encryption endpoints
    test_encryption_endpoints()
    
    # Test admin management and get auth headers
    admin_id, headers = test_admin_management()
    if not headers:
        print("\n❌ Admin authentication failed. Cannot proceed with other tests.")
        return
    
    # Test other entities
    parent_id = test_parent_management(headers)
    driver_id = test_driver_management(headers)
    route_id = test_route_management(headers)
    bus_id = test_bus_management(headers, driver_id, route_id)
    stop_id = test_route_stops_management(headers, route_id)
    
    # Create a second stop for drop-off
    if route_id:
        stop_data = {
            "route_id": route_id,
            "stop_name": "School Gate",
            "latitude": 19.0800,
            "longitude": 72.8800,
            "stop_order": 2
        }
        try:
            response = requests.post(f"{BASE_URL}/route-stops", json=stop_data, headers=headers)
            if response.status_code == 201:
                drop_stop_id = response.json()["stop_id"]
                print_test_result("Create Drop Stop", True, f"Drop Stop ID: {drop_stop_id}")
            else:
                drop_stop_id = stop_id  # Use same stop for both pickup and drop
        except:
            drop_stop_id = stop_id
    else:
        drop_stop_id = stop_id
    
    student_id = test_student_management(headers, parent_id, route_id, stop_id, drop_stop_id)
    trip_id = test_trip_management(headers, bus_id, driver_id, route_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"✅ Database Connection: Working")
    print(f"✅ Admin Management: {'Working' if admin_id else 'Failed'}")
    print(f"✅ Parent Management: {'Working' if parent_id else 'Failed'}")
    print(f"✅ Driver Management: {'Working' if driver_id else 'Failed'}")
    print(f"✅ Route Management: {'Working' if route_id else 'Failed'}")
    print(f"✅ Bus Management: {'Working' if bus_id else 'Failed'}")
    print(f"✅ Route Stops Management: {'Working' if stop_id else 'Failed'}")
    print(f"✅ Student Management: {'Working' if student_id else 'Failed'}")
    print(f"✅ Trip Management: {'Working' if trip_id else 'Failed'}")
    
    print("\n🎉 API Testing Complete!")
    print("📖 Visit http://localhost:8080/docs for interactive API documentation")

if __name__ == "__main__":
    main()