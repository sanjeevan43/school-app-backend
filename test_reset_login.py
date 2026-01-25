#!/usr/bin/env python3
"""
Test login with reset credentials
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_login_with_reset_credentials():
    """Test login with the reset admin credentials"""
    
    # Test with reset credentials
    login_data = {
        "phone": 9876543210,
        "password": "admin123"
    }
    
    print(f"Testing login with reset credentials:")
    print(f"Phone: {login_data['phone']}")
    print(f"Password: {login_data['password']}")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"\\nStatus: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"\\nSUCCESS! Login working!")
            print(f"Access Token: {token_data['access_token'][:50]}...")
            print(f"Token Type: {token_data['token_type']}")
            
            # Test using the token
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            profile_response = requests.get(f"{BASE_URL}/admins/profile", headers=headers)
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"\\nProfile retrieved successfully:")
                print(f"Name: {profile['name']}")
                print(f"Email: {profile['email']}")
            else:
                print(f"\\nProfile retrieval failed: {profile_response.status_code}")
                
        else:
            print("\\nFAILED: Login still not working")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_login_with_reset_credentials()