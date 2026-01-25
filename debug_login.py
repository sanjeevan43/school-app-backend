#!/usr/bin/env python3
"""
Debug login issue
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def debug_login():
    """Debug the login issue"""
    
    # Test with the admin we know exists
    login_data = {
        "phone": 9876543210,
        "password": "Rahul@12345"
    }
    
    print(f"Testing login with: {login_data}")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"SUCCESS: Token received: {token[:50]}...")
        else:
            print("FAILED: Login failed")
            
            # Let's check if the admin exists
            print("\nChecking if admin exists...")
            response = requests.get(f"{BASE_URL}/admins")
            if response.status_code == 200:
                admins = response.json()
                print(f"Found {len(admins)} admins:")
                for admin in admins:
                    print(f"  Phone: {admin['phone']}, Name: {admin['name']}")
            else:
                print(f"Cannot get admins: {response.status_code}")
                
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_login()