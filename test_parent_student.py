#!/usr/bin/env python3
"""
Test the new student_id functionality in parents
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_parent_student_assignment():
    """Test parent-student assignment functionality"""
    
    print("Testing Parent-Student Assignment...\n")
    
    # First, login as admin to get token
    admin_login = {"phone": 9876543210, "password": "admin123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    
    if response.status_code != 200:
        print("Failed to login as admin")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create a new parent with student_id
    print("1. Creating parent with student_id...")
    parent_data = {
        "phone": 9111111111,
        "email": "testparent@example.com",
        "name": "Test Parent With Student",
        "password": "parent123",
        "dob": "1985-05-15",
        "parent_role": "MOTHER",
        "city": "Mumbai",
        "student_id": None  # Will assign later
    }
    
    try:
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        if response.status_code == 201:
            parent = response.json()
            parent_id = parent["parent_id"]
            print(f"   SUCCESS: Parent created with ID: {parent_id}")
            print(f"   Student ID: {parent.get('student_id', 'None')}")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"   ERROR: {e}")
        return
    
    # 2. Get a student ID to assign
    print("\\n2. Getting available students...")
    try:
        response = requests.get(f"{BASE_URL}/students", headers=headers)
        if response.status_code == 200:
            students = response.json()
            if students:
                student_id = students[0]["student_id"]
                student_name = students[0]["name"]
                print(f"   Found student: {student_name} (ID: {student_id})")
            else:
                print("   No students found, creating one...")
                # Create a student first
                return
        else:
            print(f"   FAILED to get students: {response.status_code}")
            return
    except Exception as e:
        print(f"   ERROR: {e}")
        return
    
    # 3. Assign student to parent
    print("\\n3. Assigning student to parent...")
    try:
        assign_data = {"student_id": student_id}
        response = requests.put(f"{BASE_URL}/parents/{parent_id}/assign-student", 
                              json=assign_data, headers=headers)
        
        if response.status_code == 200:
            updated_parent = response.json()
            print(f"   SUCCESS: Student assigned to parent")
            print(f"   Parent: {updated_parent['name']}")
            print(f"   Assigned Student ID: {updated_parent['student_id']}")
        else:
            print(f"   FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # 4. Update parent with different student_id
    print("\\n4. Testing parent update with student_id...")
    try:
        update_data = {"city": "Delhi", "student_id": student_id}
        response = requests.put(f"{BASE_URL}/parents/{parent_id}", 
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

if __name__ == "__main__":
    test_parent_student_assignment()