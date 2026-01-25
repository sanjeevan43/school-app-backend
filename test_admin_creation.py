#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Admin Creation with the exact data from the error
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_admin_creation():
    """Test creating admin with the exact data that caused the error"""
    
    admin_data = {
        "phone": 9876543210,
        "email": "rahul.kumar@example.com",
        "name": "Rahul Kumar",
        "dob": "2002-08-14",
        "password": "Rahul@12345"
    }
    
    print("Testing Admin Creation...")
    print(f"Password length: {len(admin_data['password'])} characters")
    print(f"Password bytes: {len(admin_data['password'].encode('utf-8'))} bytes")
    
    try:
        response = requests.post(f"{BASE_URL}/admins", json=admin_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            admin = response.json()
            print("SUCCESS: Admin created successfully!")
            print(f"Admin ID: {admin['admin_id']}")
            print(f"Name: {admin['name']}")
            print(f"Email: {admin['email']}")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("SUCCESS: Admin already exists (expected)")
            return True
        else:
            print(f"FAILED: Failed to create admin: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"EXCEPTION: Exception occurred: {e}")
        return False

if __name__ == "__main__":
    test_admin_creation()