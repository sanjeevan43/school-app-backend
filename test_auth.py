#!/usr/bin/env python3
"""
Test authentication - Create admin and test login
"""

import requests
import json

BASE_URL = "http://localhost:8080/api/v1"

def test_auth():
    print("🔧 Testing Authentication...")
    
    # 1. Create admin first
    admin_data = {
        "phone": 9876543210,
        "email": "admin@school.com", 
        "name": "Test Admin",
        "password": "admin123",
        "dob": "1990-01-01"
    }
    
    print("1️⃣ Creating admin...")
    try:
        response = requests.post(f"{BASE_URL}/admins", json=admin_data)
        if response.status_code == 201:
            print("✅ Admin created successfully")
            admin = response.json()
            print(f"   Admin ID: {admin['admin_id']}")
        elif response.status_code == 400 and "already registered" in response.text:
            print("⚠️  Admin already exists")
        else:
            print(f"❌ Failed to create admin: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        return
    
    # 2. Test login
    login_data = {
        "phone": 9876543210,
        "password": "admin123"
    }
    
    print("\n2️⃣ Testing login...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            print(f"   Access Token: {token_data['access_token'][:50]}...")
            print(f"   Token Type: {token_data['token_type']}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error during login: {e}")

if __name__ == "__main__":
    test_auth()