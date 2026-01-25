#!/usr/bin/env python3
"""
Complete test for parent-student assignment with data creation
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def get_admin_token():
    """Get admin token for authentication"""
    admin_login = {"phone": 9876543210, "password": "admin123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def create_test_data(headers):
    """Create necessary test data"""
    print("Creating test data...")
    
    # Create route
    route_data = {"name": "Test Route for Parent-Student"}
    response = requests.post(f"{BASE_URL}/routes", json=route_data, headers=headers)
    if response.status_code == 201:
        route_id = response.json()["route_id"]
        print(f"   Route created: {route_id}")
    else:
        print("   Using existing route...")
        response = requests.get(f"{BASE_URL}/routes", headers=headers)
        routes = response.json()
        route_id = routes[0]["route_id"] if routes else None
    
    if not route_id:
        print("   ERROR: No route available")
        return None, None, None
    
    # Create route stops
    stop1_data = {
        "route_id": route_id,
        "stop_name": "Test Stop 1",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "stop_order": 1
    }
    
    stop2_data = {
        "route_id": route_id,
        "stop_name": "Test Stop 2", 
        "latitude": 12.9716,
        "longitude": 77.5946,
        "stop_order": 2
    }
    
    response1 = requests.post(f"{BASE_URL}/route-stops", json=stop1_data, headers=headers)
    response2 = requests.post(f"{BASE_URL}/route-stops", json=stop2_data, headers=headers)
    
    if response1.status_code == 201 and response2.status_code == 201:
        stop1_id = response1.json()["stop_id"]
        stop2_id = response2.json()["stop_id"]
        print(f"   Stops created: {stop1_id}, {stop2_id}")
    else:
        # Get existing stops
        response = requests.get(f"{BASE_URL}/route-stops?route_id={route_id}", headers=headers)
        stops = response.json()
        if len(stops) >= 2:
            stop1_id = stops[0]["stop_id"]
            stop2_id = stops[1]["stop_id"]
        else:
            print("   ERROR: Not enough stops")
            return None, None, None
    
    # Create parent for student
    parent_data = {
        "phone": 9222222222,
        "email": "studentparent@example.com",
        "name": "Student Parent",
        "password": "parent123",
        "dob": "1985-05-15",
        "parent_role": "FATHER",
        "city": "Bangalore"
    }
    
    response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
    if response.status_code == 201:
        parent_id = response.json()["parent_id"]
        print(f"   Parent created: {parent_id}")
    else:
        print("   Using existing parent...")
        response = requests.get(f"{BASE_URL}/parents", headers=headers)
        parents = response.json()
        parent_id = parents[0]["parent_id"] if parents else None
    
    # Create student
    student_data = {
        "parent_id": parent_id,
        "name": "Test Student",
        "dob": "2010-01-01",
        "class_section": "5A",
        "route_id": route_id,
        "pickup_stop_id": stop1_id,
        "drop_stop_id": stop2_id
    }
    
    response = requests.post(f"{BASE_URL}/students", json=student_data, headers=headers)
    if response.status_code == 201:
        student_id = response.json()["student_id"]
        print(f"   Student created: {student_id}")
        return route_id, parent_id, student_id
    else:
        print(f"   ERROR creating student: {response.text}")
        return None, None, None

def test_complete_parent_student():
    """Complete test for parent-student functionality"""
    
    print("=== Testing Parent-Student Assignment ===\\n")
    
    # Get admin token
    token = get_admin_token()
    if not token:
        print("Failed to get admin token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create test data
    route_id, existing_parent_id, student_id = create_test_data(headers)
    if not all([route_id, existing_parent_id, student_id]):
        print("Failed to create test data")
        return
    
    print(f"\\nTest data created:")
    print(f"  Route ID: {route_id}")
    print(f"  Parent ID: {existing_parent_id}")
    print(f"  Student ID: {student_id}")
    
    # 1. Create a new parent with student_id in creation
    print("\\n1. Creating parent with student_id during creation...")
    parent_data = {
        "phone": 9333333333,
        "email": "newparent@example.com",
        "name": "New Parent With Student",
        "password": "parent123",
        "dob": "1985-05-15",
        "parent_role": "MOTHER",
        "city": "Mumbai",
        "student_id": student_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        if response.status_code == 201:
            new_parent = response.json()
            new_parent_id = new_parent["parent_id"]
            print(f"   SUCCESS: Parent created with ID: {new_parent_id}")
            print(f"   Student ID: {new_parent.get('student_id')}")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"   ERROR: {e}")
        return
    
    # 2. Use assign-student endpoint
    print("\\n2. Testing assign-student endpoint...")
    try:
        assign_data = {"student_id": student_id}
        response = requests.put(f"{BASE_URL}/parents/{existing_parent_id}/assign-student", 
                              json=assign_data, headers=headers)
        
        if response.status_code == 200:
            updated_parent = response.json()
            print(f"   SUCCESS: Student assigned to existing parent")
            print(f"   Parent: {updated_parent['name']}")
            print(f"   Assigned Student ID: {updated_parent['student_id']}")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # 3. Update parent with student_id
    print("\\n3. Testing parent update with student_id...")
    try:
        update_data = {"city": "Delhi", "student_id": student_id}
        response = requests.put(f"{BASE_URL}/parents/{new_parent_id}", 
                              json=update_data, headers=headers)
        
        if response.status_code == 200:
            updated_parent = response.json()
            print(f"   SUCCESS: Parent updated")
            print(f"   City: {updated_parent['city']}")
            print(f"   Student ID: {updated_parent['student_id']}")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # 4. Get parent and verify student_id is included
    print("\\n4. Verifying student_id in parent response...")
    try:
        response = requests.get(f"{BASE_URL}/parents/{new_parent_id}", headers=headers)
        if response.status_code == 200:
            parent = response.json()
            print(f"   SUCCESS: Parent retrieved")
            print(f"   Name: {parent['name']}")
            print(f"   Student ID: {parent.get('student_id', 'None')}")
        else:
            print(f"   FAILED: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\\n=== Test Complete ===")

if __name__ == "__main__":
    test_complete_parent_student()