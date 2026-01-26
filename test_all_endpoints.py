#!/usr/bin/env python3
"""
Enhanced Complete API Test Script
Tests all endpoints and saves detailed results
"""

import requests
import json
from datetime import date, datetime
import sys

BASE_URL = "http://localhost:8080/api/v1"
RESULTS = []

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def log_result(category, test_name, success, message="", response_data=None):
    """Log test result"""
    status = f"{Colors.GREEN}✅{Colors.RESET}" if success else f"{Colors.RED}❌{Colors.RESET}"
    result = {
        "category": category,
        "test": test_name,
        "success": success,
        "message": message,
        "data": response_data
    }
    RESULTS.append(result)
    print(f"{status} {category} - {test_name}")
    if message:
        print(f"   {message}")
    return success

def test_health_check():
    """Test health and database connection"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🏥 HEALTH CHECK{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        data = response.json()
        success = response.status_code == 200 and data.get("database") == "connected"
        return log_result("Health", "Database Connection", success, 
                         f"Status: {data.get('status')}, DB: {data.get('database')}")
    except Exception as e:
        return log_result("Health", "Database Connection", False, f"Error: {str(e)}")

def test_encryption():
    """Test encryption/decryption endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🔐 ENCRYPTION/DECRYPTION{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    try:
        # Test encryption
        test_text = "Hello World Test 123"
        response = requests.post(f"{BASE_URL}/encrypt", json={"text": test_text})
        
        if response.status_code == 200:
            encrypted = response.json()["encrypted_text"]
            log_result("Encryption", "Encrypt Text", True, f"Encrypted: {encrypted[:30]}...")
            
            # Test decryption
            response = requests.post(f"{BASE_URL}/decrypt", json={"encrypted_text": encrypted})
            if response.status_code == 200:
                decrypted = response.json()["decrypted_text"]
                success = decrypted == test_text
                log_result("Encryption", "Decrypt Text", success, 
                          f"Decrypted: {decrypted}")
                return success
        
        log_result("Encryption", "Encrypt/Decrypt", False, f"Status: {response.status_code}")
        return False
    except Exception as e:
        log_result("Encryption", "Encrypt/Decrypt", False, f"Error: {str(e)}")
        return False

def test_admin_endpoints():
    """Test all admin endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}👨‍💼 ADMIN ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    admin_data = {
        "phone": 9876543210,
        "email": "admin@test.com",
        "name": "Test Admin",
        "password": "admin123",
        "dob": "1990-01-01"
    }
    
    try:
        # 1. Create Admin
        response = requests.post(f"{BASE_URL}/admins", json=admin_data)
        if response.status_code == 201:
            admin = response.json()
            admin_id = admin["admin_id"]
            log_result("Admin", "POST /admins (Create)", True, f"ID: {admin_id}")
        elif response.status_code == 400 and "already registered" in response.text:
            log_result("Admin", "POST /admins (Create)", True, "Admin already exists")
            admin_id = None
        else:
            log_result("Admin", "POST /admins (Create)", False, f"Status: {response.status_code}")
            return None, None
        
        # 2. Admin Login
        login_data = {"phone": 9876543210, "password": "admin123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            log_result("Admin", "POST /auth/login", True, "Token received")
        else:
            log_result("Admin", "POST /auth/login", False, f"Status: {response.status_code}")
            return None, None
        
        # 3. Get Admin Profile
        response = requests.get(f"{BASE_URL}/admins/profile", headers=headers)
        log_result("Admin", "GET /admins/profile", response.status_code == 200)
        
        # 4. Get All Admins
        response = requests.get(f"{BASE_URL}/admins", headers=headers)
        if response.status_code == 200:
            admins = response.json()
            log_result("Admin", "GET /admins", True, f"Found {len(admins)} admin(s)")
            if not admin_id and admins:
                admin_id = admins[0]["admin_id"]
        else:
            log_result("Admin", "GET /admins", False)
        
        # 5. Get Admin by ID
        if admin_id:
            response = requests.get(f"{BASE_URL}/admins/{admin_id}", headers=headers)
            log_result("Admin", f"GET /admins/{{id}}", response.status_code == 200)
        
        # 6. Update Admin
        if admin_id:
            update_data = {"name": "Updated Admin"}
            response = requests.put(f"{BASE_URL}/admins/{admin_id}", json=update_data, headers=headers)
            log_result("Admin", f"PUT /admins/{{id}}", response.status_code == 200)
        
        return admin_id, headers
        
    except Exception as e:
        log_result("Admin", "Admin Endpoints", False, f"Error: {str(e)}")
        return None, None

def test_parent_endpoints(headers):
    """Test all parent endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}👨‍👩‍👧‍👦 PARENT ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    parent_data = {
        "phone": 9123456789,
        "email": "parent@test.com",
        "name": "Test Parent",
        "password": "parent123",
        "dob": "1985-05-15",
        "parent_role": "MOTHER",
        "city": "Mumbai"
    }
    
    try:
        # 1. Create Parent
        response = requests.post(f"{BASE_URL}/parents", json=parent_data, headers=headers)
        if response.status_code == 201:
            parent = response.json()
            parent_id = parent["parent_id"]
            log_result("Parent", "POST /parents (Create)", True, f"ID: {parent_id}")
        elif response.status_code == 400 and "already registered" in response.text:
            log_result("Parent", "POST /parents (Create)", True, "Parent already exists")
            # Get existing parent
            response = requests.get(f"{BASE_URL}/parents", headers=headers)
            if response.status_code == 200:
                parents = response.json()
                parent_id = parents[0]["parent_id"] if parents else None
            else:
                parent_id = None
        else:
            log_result("Parent", "POST /parents (Create)", False, f"Status: {response.status_code}")
            return None
        
        # 2. Parent Login
        login_data = {"phone": 9123456789, "password": "parent123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        log_result("Parent", "POST /auth/login (Parent)", response.status_code == 200)
        
        # 3. Get All Parents
        response = requests.get(f"{BASE_URL}/parents", headers=headers)
        if response.status_code == 200:
            parents = response.json()
            log_result("Parent", "GET /parents", True, f"Found {len(parents)} parent(s)")
        else:
            log_result("Parent", "GET /parents", False)
        
        # 4. Get Parent by ID
        if parent_id:
            response = requests.get(f"{BASE_URL}/parents/{parent_id}", headers=headers)
            log_result("Parent", "GET /parents/{id}", response.status_code == 200)
        
        # 5. Update Parent
        if parent_id:
            update_data = {"city": "Delhi"}
            response = requests.put(f"{BASE_URL}/parents/{parent_id}", json=update_data, headers=headers)
            log_result("Parent", "PUT /parents/{id}", response.status_code == 200)
        
        return parent_id
        
    except Exception as e:
        log_result("Parent", "Parent Endpoints", False, f"Error: {str(e)}")
        return None

def test_driver_endpoints(headers):
    """Test all driver endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🚗 DRIVER ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    driver_data = {
        "name": "Test Driver",
        "phone": 9987654321,
        "email": "driver@test.com",
        "password": "driver123",
        "dob": "1980-03-20",
        "licence_number": "DL123456789",
        "licence_expiry": "2025-12-31",
        "aadhar_number": "123456789012"
    }
    
    try:
        # 1. Create Driver
        response = requests.post(f"{BASE_URL}/drivers", json=driver_data, headers=headers)
        if response.status_code == 201:
            driver = response.json()
            driver_id = driver["driver_id"]
            log_result("Driver", "POST /drivers (Create)", True, f"ID: {driver_id}")
        elif response.status_code == 400 and "already registered" in response.text:
            log_result("Driver", "POST /drivers (Create)", True, "Driver already exists")
            response = requests.get(f"{BASE_URL}/drivers", headers=headers)
            if response.status_code == 200:
                drivers = response.json()
                driver_id = drivers[0]["driver_id"] if drivers else None
            else:
                driver_id = None
        else:
            log_result("Driver", "POST /drivers (Create)", False, f"Status: {response.status_code}")
            return None
        
        # 2. Driver Login
        login_data = {"phone": 9987654321, "password": "driver123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        log_result("Driver", "POST /auth/login (Driver)", response.status_code == 200)
        
        # 3. Get All Drivers
        response = requests.get(f"{BASE_URL}/drivers", headers=headers)
        if response.status_code == 200:
            drivers = response.json()
            log_result("Driver", "GET /drivers", True, f"Found {len(drivers)} driver(s)")
        else:
            log_result("Driver", "GET /drivers", False)
        
        # 4. Get Available Drivers
        response = requests.get(f"{BASE_URL}/drivers/available", headers=headers)
        log_result("Driver", "GET /drivers/available", response.status_code == 200)
        
        # 5. Get Driver by ID
        if driver_id:
            response = requests.get(f"{BASE_URL}/drivers/{driver_id}", headers=headers)
            log_result("Driver", "GET /drivers/{id}", response.status_code == 200)
        
        # 6. Update Driver
        if driver_id:
            update_data = {"is_available": True}
            response = requests.put(f"{BASE_URL}/drivers/{driver_id}", json=update_data, headers=headers)
            log_result("Driver", "PUT /drivers/{id}", response.status_code == 200)
        
        return driver_id
        
    except Exception as e:
        log_result("Driver", "Driver Endpoints", False, f"Error: {str(e)}")
        return None

def test_route_endpoints(headers):
    """Test all route endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🛣️ ROUTE ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    route_data = {"name": "Route A - Main Street"}
    
    try:
        # 1. Create Route
        response = requests.post(f"{BASE_URL}/routes", json=route_data, headers=headers)
        if response.status_code == 201:
            route = response.json()
            route_id = route["route_id"]
            log_result("Route", "POST /routes (Create)", True, f"ID: {route_id}")
        else:
            log_result("Route", "POST /routes (Create)", False, f"Status: {response.status_code}")
            # Try to get existing route
            response = requests.get(f"{BASE_URL}/routes", headers=headers)
            if response.status_code == 200:
                routes = response.json()
                route_id = routes[0]["route_id"] if routes else None
            else:
                route_id = None
        
        # 2. Get All Routes
        response = requests.get(f"{BASE_URL}/routes", headers=headers)
        if response.status_code == 200:
            routes = response.json()
            log_result("Route", "GET /routes", True, f"Found {len(routes)} route(s)")
        else:
            log_result("Route", "GET /routes", False)
        
        # 3. Get Route by ID
        if route_id:
            response = requests.get(f"{BASE_URL}/routes/{route_id}", headers=headers)
            log_result("Route", "GET /routes/{id}", response.status_code == 200)
        
        # 4. Update Route
        if route_id:
            update_data = {"name": "Route A - Updated"}
            response = requests.put(f"{BASE_URL}/routes/{route_id}", json=update_data, headers=headers)
            log_result("Route", "PUT /routes/{id}", response.status_code == 200)
        
        return route_id
        
    except Exception as e:
        log_result("Route", "Route Endpoints", False, f"Error: {str(e)}")
        return None

def test_bus_endpoints(headers, driver_id, route_id):
    """Test all bus endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🚌 BUS ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    if not driver_id or not route_id:
        log_result("Bus", "Bus Endpoints", False, "Missing driver or route ID")
        return None
    
    bus_data = {
        "bus_number": "MH01AB1234",
        "driver_id": driver_id,
        "route_id": route_id,
        "bus_type": "AC",
        "bus_brand": "Tata",
        "bus_model": "Starbus",
        "seating_capacity": 40,
        "rc_expiry_date": "2025-12-31",
        "fc_expiry_date": "2024-12-31"
    }
    
    try:
        # 1. Create Bus
        response = requests.post(f"{BASE_URL}/buses", json=bus_data, headers=headers)
        if response.status_code == 201:
            bus = response.json()
            bus_id = bus["bus_id"]
            log_result("Bus", "POST /buses (Create)", True, f"ID: {bus_id}")
        elif response.status_code == 400:
            log_result("Bus", "POST /buses (Create)", True, "Bus already exists")
            response = requests.get(f"{BASE_URL}/buses", headers=headers)
            if response.status_code == 200:
                buses = response.json()
                bus_id = buses[0]["bus_id"] if buses else None
            else:
                bus_id = None
        else:
            log_result("Bus", "POST /buses (Create)", False, f"Status: {response.status_code}")
            return None
        
        # 2. Get All Buses
        response = requests.get(f"{BASE_URL}/buses", headers=headers)
        if response.status_code == 200:
            buses = response.json()
            log_result("Bus", "GET /buses", True, f"Found {len(buses)} bus(es)")
        else:
            log_result("Bus", "GET /buses", False)
        
        # 3. Get Bus by ID
        if bus_id:
            response = requests.get(f"{BASE_URL}/buses/{bus_id}", headers=headers)
            log_result("Bus", "GET /buses/{id}", response.status_code == 200)
        
        # 4. Update Bus
        if bus_id:
            update_data = {"seating_capacity": 45}
            response = requests.put(f"{BASE_URL}/buses/{bus_id}", json=update_data, headers=headers)
            log_result("Bus", "PUT /buses/{id}", response.status_code == 200)
        
        return bus_id
        
    except Exception as e:
        log_result("Bus", "Bus Endpoints", False, f"Error: {str(e)}")
        return None

def test_route_stop_endpoints(headers, route_id):
    """Test all route stop endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🚏 ROUTE STOP ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    if not route_id:
        log_result("RouteStop", "Route Stop Endpoints", False, "Missing route ID")
        return None, None
    
    stop_data = {
        "route_id": route_id,
        "stop_name": "Main Gate",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "stop_order": 1
    }
    
    try:
        # 1. Create Route Stop
        response = requests.post(f"{BASE_URL}/route-stops", json=stop_data, headers=headers)
        if response.status_code == 201:
            stop = response.json()
            stop_id = stop["stop_id"]
            log_result("RouteStop", "POST /route-stops (Create)", True, f"ID: {stop_id}")
        else:
            log_result("RouteStop", "POST /route-stops (Create)", False, f"Status: {response.status_code}")
            response = requests.get(f"{BASE_URL}/route-stops", headers=headers)
            if response.status_code == 200:
                stops = response.json()
                stop_id = stops[0]["stop_id"] if stops else None
            else:
                stop_id = None
        
        # 2. Get All Route Stops
        response = requests.get(f"{BASE_URL}/route-stops", headers=headers)
        if response.status_code == 200:
            stops = response.json()
            log_result("RouteStop", "GET /route-stops", True, f"Found {len(stops)} stop(s)")
        else:
            log_result("RouteStop", "GET /route-stops", False)
        
        # 3. Get Route Stops by Route
        response = requests.get(f"{BASE_URL}/route-stops?route_id={route_id}", headers=headers)
        log_result("RouteStop", "GET /route-stops?route_id={id}", response.status_code == 200)
        
        # 4. Create second stop for drop-off
        drop_stop_data = {
            "route_id": route_id,
            "stop_name": "School Gate",
            "latitude": 19.0800,
            "longitude": 72.8800,
            "stop_order": 2
        }
        response = requests.post(f"{BASE_URL}/route-stops", json=drop_stop_data, headers=headers)
        if response.status_code == 201:
            drop_stop = response.json()
            drop_stop_id = drop_stop["stop_id"]
            log_result("RouteStop", "POST /route-stops (Drop Stop)", True, f"ID: {drop_stop_id}")
        else:
            drop_stop_id = stop_id
        
        # 5. Update Route Stop
        if stop_id:
            update_data = {"stop_name": "Main Gate Updated"}
            response = requests.put(f"{BASE_URL}/route-stops/{stop_id}", json=update_data, headers=headers)
            log_result("RouteStop", "PUT /route-stops/{id}", response.status_code == 200)
        
        return stop_id, drop_stop_id
        
    except Exception as e:
        log_result("RouteStop", "Route Stop Endpoints", False, f"Error: {str(e)}")
        return None, None

def test_student_endpoints(headers, parent_id, route_id, pickup_stop_id, drop_stop_id):
    """Test all student endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}👨‍🎓 STUDENT ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    if not all([parent_id, route_id, pickup_stop_id, drop_stop_id]):
        log_result("Student", "Student Endpoints", False, "Missing required IDs")
        return None
    
    student_data = {
        "parent_id": parent_id,
        "name": "Test Student",
        "dob": "2010-01-01",
        "class_section": "5A",
        "route_id": route_id,
        "pickup_stop_id": pickup_stop_id,
        "drop_stop_id": drop_stop_id
    }
    
    try:
        # 1. Create Student
        response = requests.post(f"{BASE_URL}/students", json=student_data, headers=headers)
        if response.status_code == 201:
            student = response.json()
            student_id = student["student_id"]
            log_result("Student", "POST /students (Create)", True, f"ID: {student_id}")
        else:
            log_result("Student", "POST /students (Create)", False, f"Status: {response.status_code}")
            response = requests.get(f"{BASE_URL}/students", headers=headers)
            if response.status_code == 200:
                students = response.json()
                student_id = students[0]["student_id"] if students else None
            else:
                student_id = None
        
        # 2. Get All Students
        response = requests.get(f"{BASE_URL}/students", headers=headers)
        if response.status_code == 200:
            students = response.json()
            log_result("Student", "GET /students", True, f"Found {len(students)} student(s)")
        else:
            log_result("Student", "GET /students", False)
        
        # 3. Get Students by Parent
        response = requests.get(f"{BASE_URL}/students/parent/{parent_id}", headers=headers)
        log_result("Student", "GET /students/parent/{id}", response.status_code == 200)
        
        # 4. Get Student by ID
        if student_id:
            response = requests.get(f"{BASE_URL}/students/{student_id}", headers=headers)
            log_result("Student", "GET /students/{id}", response.status_code == 200)
        
        # 5. Update Student
        if student_id:
            update_data = {"class_section": "6A"}
            response = requests.put(f"{BASE_URL}/students/{student_id}", json=update_data, headers=headers)
            log_result("Student", "PUT /students/{id}", response.status_code == 200)
        
        return student_id
        
    except Exception as e:
        log_result("Student", "Student Endpoints", False, f"Error: {str(e)}")
        return None

def test_trip_endpoints(headers, bus_id, driver_id, route_id):
    """Test all trip endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🚌 TRIP ENDPOINTS{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    if not all([bus_id, driver_id, route_id]):
        log_result("Trip", "Trip Endpoints", False, "Missing required IDs")
        return None
    
    trip_data = {
        "bus_id": bus_id,
        "driver_id": driver_id,
        "route_id": route_id,
        "trip_date": "2024-01-15",
        "trip_type": "MORNING"
    }
    
    try:
        # 1. Create Trip
        response = requests.post(f"{BASE_URL}/trips", json=trip_data, headers=headers)
        if response.status_code == 201:
            trip = response.json()
            trip_id = trip["trip_id"]
            log_result("Trip", "POST /trips (Create)", True, f"ID: {trip_id}")
        else:
            log_result("Trip", "POST /trips (Create)", False, f"Status: {response.status_code}")
            response = requests.get(f"{BASE_URL}/trips", headers=headers)
            if response.status_code == 200:
                trips = response.json()
                trip_id = trips[0]["trip_id"] if trips else None
            else:
                trip_id = None
        
        # 2. Get All Trips
        response = requests.get(f"{BASE_URL}/trips", headers=headers)
        if response.status_code == 200:
            trips = response.json()
            log_result("Trip", "GET /trips", True, f"Found {len(trips)} trip(s)")
        else:
            log_result("Trip", "GET /trips", False)
        
        # 3. Get Trips by Route
        response = requests.get(f"{BASE_URL}/trips?route_id={route_id}", headers=headers)
        log_result("Trip", "GET /trips?route_id={id}", response.status_code == 200)
        
        # 4. Get Trip by ID
        if trip_id:
            response = requests.get(f"{BASE_URL}/trips/{trip_id}", headers=headers)
            log_result("Trip", "GET /trips/{id}", response.status_code == 200)
        
        # 5. Update Trip
        if trip_id:
            update_data = {"trip_type": "EVENING"}
            response = requests.put(f"{BASE_URL}/trips/{trip_id}", json=update_data, headers=headers)
            log_result("Trip", "PUT /trips/{id}", response.status_code == 200)
        
        return trip_id
        
    except Exception as e:
        log_result("Trip", "Trip Endpoints", False, f"Error: {str(e)}")
        return None

def print_summary():
    """Print test summary"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}📊 TEST SUMMARY{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    # Group by category
    categories = {}
    for result in RESULTS:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = {"passed": 0, "failed": 0, "total": 0}
        categories[cat]["total"] += 1
        if result["success"]:
            categories[cat]["passed"] += 1
        else:
            categories[cat]["failed"] += 1
    
    # Print category summary
    total_passed = 0
    total_failed = 0
    
    for cat, stats in categories.items():
        status = f"{Colors.GREEN}✅{Colors.RESET}" if stats["failed"] == 0 else f"{Colors.YELLOW}⚠️{Colors.RESET}"
        print(f"{status} {cat:15} - Passed: {stats['passed']:2}/{stats['total']:2}")
        total_passed += stats["passed"]
        total_failed += stats["failed"]
    
    # Overall summary
    total_tests = total_passed + total_failed
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"Total Tests: {total_tests}")
    print(f"{Colors.GREEN}Passed: {total_passed}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {total_failed}{Colors.RESET}")
    print(f"Success Rate: {success_rate:.1f}%")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    # Save detailed results to file
    with open("test_results.json", "w") as f:
        json.dump(RESULTS, f, indent=2, default=str)
    print(f"📄 Detailed results saved to: test_results.json")
    
    return total_failed == 0

def main():
    """Main test runner"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}🚀 SCHOOL TRANSPORT API - COMPLETE TEST SUITE{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    if not test_health_check():
        print(f"\n{Colors.RED}❌ Database connection failed. Exiting.{Colors.RESET}\n")
        return False
    
    test_encryption()
    
    admin_id, headers = test_admin_endpoints()
    if not headers:
        print(f"\n{Colors.RED}❌ Admin authentication failed. Exiting.{Colors.RESET}\n")
        return False
    
    parent_id = test_parent_endpoints(headers)
    driver_id = test_driver_endpoints(headers)
    route_id = test_route_endpoints(headers)
    bus_id = test_bus_endpoints(headers, driver_id, route_id)
    pickup_stop_id, drop_stop_id = test_route_stop_endpoints(headers, route_id)
    student_id = test_student_endpoints(headers, parent_id, route_id, pickup_stop_id, drop_stop_id)
    trip_id = test_trip_endpoints(headers, bus_id, driver_id, route_id)
    
    # Print summary
    success = print_summary()
    
    if success:
        print(f"{Colors.GREEN}🎉 All tests passed!{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}⚠️ Some tests failed. Check test_results.json for details.{Colors.RESET}\n")
    
    print(f"📖 API Documentation: http://localhost:8080/docs\n")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {str(e)}{Colors.RESET}\n")
        sys.exit(1)
