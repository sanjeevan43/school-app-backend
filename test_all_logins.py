#!/usr/bin/env python3
"""
Test login for all user types
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_all_logins():
    """Test login for all user types"""
    
    print("Testing login for all user types...\n")
    
    # Test Admin Login
    print("1. Testing Admin Login...")
    admin_login = {"phone": 9876543210, "password": "admin123"}
    test_login(admin_login, "Admin")
    
    # Test Parent Login
    print("\n2. Testing Parent Login...")
    parent_login = {"phone": 9123456788, "password": "parent123"}
    test_login(parent_login, "Parent")
    
    # Test Driver Login
    print("\n3. Testing Driver Login...")
    driver_login = {"phone": 9987654322, "password": "driver123"}
    test_login(driver_login, "Driver")

def test_login(login_data, user_type):
    """Test login for a specific user"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"   SUCCESS: {user_type} login working!")
            print(f"   Token: {token_data['access_token'][:30]}...")
            return token_data['access_token']
        else:
            print(f"   FAILED: {user_type} login failed")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ERROR: {e}")
        return None

if __name__ == "__main__":
    test_all_logins()