#!/usr/bin/env python3
"""
Test all POST endpoints that use password hashing
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_all_password_endpoints():
    """Test all endpoints that create users with passwords"""
    
    print("Testing all POST endpoints with password hashing...\n")
    
    # Test 1: Create Admin
    print("1. Testing Admin Creation...")
    admin_data = {
        "phone": 9876543211,
        "email": "admin2@test.com",
        "name": "Test Admin 2",
        "dob": "1990-01-01",
        "password": "TestAdmin@123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admins", json=admin_data)
        if response.status_code == 201:
            print("   SUCCESS: Admin created")
            admin = response.json()
            admin_token = login_user(admin_data["phone"], admin_data["password"])
        elif response.status_code == 400 and "already registered" in response.text:
            print("   SUCCESS: Admin already exists")
            admin_token = login_user(admin_data["phone"], admin_data["password"])
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
            admin_token = None
    except Exception as e:
        print(f"   ERROR: {e}")
        admin_token = None
    
    if not admin_token:
        print("Cannot proceed without admin token")
        return
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test 2: Create Parent
    print("\\n2. Testing Parent Creation...")
    parent_data = {
        "phone": 9123456788,
        "email": "parent2@test.com",
        "name": "Test Parent 2",
        "password": "TestParent@123",
        "dob": "1985-05-15",
        "parent_role": "FATHER",
        "city": "Delhi"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        if response.status_code == 201:
            print("   SUCCESS: Parent created")
        elif response.status_code == 400 and "already registered" in response.text:
            print("   SUCCESS: Parent already exists")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: Create Driver
    print("\\n3. Testing Driver Creation...")
    driver_data = {
        "name": "Test Driver 2",
        "phone": 9987654322,
        "email": "driver2@test.com",
        "password": "TestDriver@123",
        "dob": "1980-03-20",
        "licence_number": "DL987654321",
        "licence_expiry": "2025-12-31",
        "aadhar_number": "987654321012"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/drivers", json=driver_data, headers=headers)
        if response.status_code == 201:
            print("   SUCCESS: Driver created")
        elif response.status_code == 400 and "already registered" in response.text:
            print("   SUCCESS: Driver already exists")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test login for all created users
    print("\\n4. Testing Login for all user types...")
    
    # Test admin login
    if login_user(admin_data["phone"], admin_data["password"]):
        print("   SUCCESS: Admin login works")
    else:
        print("   FAILED: Admin login failed")
    
    # Test parent login
    if login_user(parent_data["phone"], parent_data["password"]):
        print("   SUCCESS: Parent login works")
    else:
        print("   FAILED: Parent login failed")
    
    # Test driver login
    if login_user(driver_data["phone"], driver_data["password"]):
        print("   SUCCESS: Driver login works")
    else:
        print("   FAILED: Driver login failed")

def login_user(phone, password):
    """Helper function to login and get token"""
    try:
        login_data = {"phone": phone, "password": password}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    except:
        return None

if __name__ == "__main__":
    test_all_password_endpoints()