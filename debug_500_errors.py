#!/usr/bin/env python3
"""
Debug 500 Internal Server Errors
"""

import requests
import json

def test_all_endpoints():
    """Test all endpoints to find 500 errors"""
    base_url = "http://127.0.0.1:8080"
    
    # Test endpoints that commonly cause 500 errors
    test_cases = [
        ("GET", "/"),
        ("GET", "/health"),
        ("GET", "/api/v1/admins"),
        ("GET", "/api/v1/parents"),
        ("GET", "/api/v1/drivers"),
        ("GET", "/api/v1/routes"),
        ("GET", "/api/v1/buses"),
        ("GET", "/api/v1/route-stops"),
        ("GET", "/api/v1/students"),
        ("GET", "/api/v1/trips"),
        ("POST", "/api/v1/auth/login", {"phone": 9876543210, "password": "test123"}),
    ]
    
    print("Testing endpoints for 500 errors...")
    errors_found = []
    
    for method, endpoint, *data in test_cases:
        try:
            url = f"{base_url}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=data[0] if data else {}, timeout=5)
            
            if response.status_code == 500:
                errors_found.append({
                    "endpoint": endpoint,
                    "method": method,
                    "error": response.text
                })
                print(f"[ERROR] {method} {endpoint} -> 500")
                print(f"Response: {response.text[:200]}...")
            else:
                print(f"[OK] {method} {endpoint} -> {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"[SKIP] {method} {endpoint} -> Server not running")
        except Exception as e:
            print(f"[FAIL] {method} {endpoint} -> {e}")
    
    return errors_found

if __name__ == "__main__":
    errors = test_all_endpoints()
    
    if errors:
        print(f"\nFound {len(errors)} endpoints with 500 errors:")
        for error in errors:
            print(f"- {error['method']} {error['endpoint']}")
    else:
        print("\nNo 500 errors found!")