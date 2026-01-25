#!/usr/bin/env python3
"""
Test parent creation with valid data
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_valid_parent_creation():
    """Test parent creation with valid data"""
    
    # Get admin token
    admin_login = {"phone": 9876543210, "password": "admin123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    
    if response.status_code != 200:
        print("Failed to get admin token")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Create parent without student_id (should work)
    print("1. Testing parent creation without student_id...")
    parent_data = {
        "phone": 9876543299,
        "email": "lakshmi.valid@example.com",
        "name": "Lakshmi Raman Valid",
        "dob": "1989-11-03",
        "parent_role": "GUARDIAN",
        "door_no": "12B",
        "street": "MG Nagar 3rd Street",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "pincode": "600042",
        "emergency_contact": 9123456780,
        "fcm_token": "fcm_valid_token",
        "password": "Lakshmi@123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        
        if response.status_code == 201:
            parent = response.json()
            print(f"   SUCCESS: Parent created!")
            print(f"   Parent ID: {parent['parent_id']}")
            print(f"   Name: {parent['name']}")
            print(f"   Student ID: {parent.get('student_id', 'None')}")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: Get a valid student ID and create parent with it
    print("\\n2. Testing parent creation with valid student_id...")
    
    try:
        # Get existing students
        response = requests.get(f"{BASE_URL}/students", headers=headers)
        if response.status_code == 200:
            students = response.json()
            if students:
                valid_student_id = students[0]["student_id"]
                print(f"   Using valid student ID: {valid_student_id}")
                
                parent_data_with_student = {
                    "phone": 9876543298,
                    "email": "lakshmi.withstudent@example.com",
                    "name": "Lakshmi With Student",
                    "dob": "1989-11-03",
                    "parent_role": "GUARDIAN",
                    "city": "Chennai",
                    "student_id": valid_student_id,
                    "password": "Lakshmi@123"
                }
                
                response = requests.post(f"{BASE_URL}/parents", json=parent_data_with_student, headers=headers)
                
                if response.status_code == 201:
                    parent = response.json()
                    print(f"   SUCCESS: Parent with student created!")
                    print(f"   Parent ID: {parent['parent_id']}")
                    print(f"   Name: {parent['name']}")
                    print(f"   Student ID: {parent.get('student_id')}")
                else:
                    print(f"   FAILED: {response.status_code} - {response.text}")
            else:
                print("   No students available for testing")
        else:
            print(f"   Could not get students: {response.status_code}")
            
    except Exception as e:
        print(f"   ERROR: {e}")

if __name__ == "__main__":
    test_valid_parent_creation()