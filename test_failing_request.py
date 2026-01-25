#!/usr/bin/env python3
"""
Test the exact parent creation request that was failing
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_failing_parent_creation():
    """Test the exact request that was failing"""
    
    # Get admin token first
    admin_login = {"phone": 9876543210, "password": "admin123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    
    if response.status_code != 200:
        print("Failed to get admin token")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # The exact data from the failing request
    parent_data = {
        "phone": 9876543210,
        "email": "lakshmi.r@example.com",
        "name": "Lakshmi Raman",
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
        "fcm_token": "fcm_c2FtcGxlX3Rva2VuX3BhcmVudF8xMjM0NTY",
        "student_id": "8f3a2c1e-4b92-4f8c-a2e1-9c4b7d2f6a11",
        "password": "Lakshmi@123"
    }
    
    print("Testing the exact failing parent creation request...")
    print(f"Phone: {parent_data['phone']}")
    print(f"Name: {parent_data['name']}")
    print(f"Student ID: {parent_data['student_id']}")
    
    try:
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        
        print(f"\\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            parent = response.json()
            print(f"\\nSUCCESS: Parent created!")
            print(f"Parent ID: {parent['parent_id']}")
            print(f"Name: {parent['name']}")
            print(f"Student ID: {parent.get('student_id')}")
        elif response.status_code == 400:
            print(f"\\nValidation Error: {response.json()}")
        else:
            print(f"\\nFAILED: {response.status_code}")
            
    except Exception as e:
        print(f"\\nERROR: {e}")

if __name__ == "__main__":
    test_failing_parent_creation()