import json
from fastapi.testclient import TestClient
from main import app
import sys

client = TestClient(app)

def run_tests():
    print("Starting comprehensive API testing (A to Z)...")
    results = {}
    
    # 1. Test Health
    print("Testing /health...")
    resp = client.get("/health")
    results["/health"] = {"status": resp.status_code, "body": resp.text[:100]}
    
    # 2. Get all endpoints from FastAPI
    routes = []
    for route in app.routes:
        if hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": route.methods
            })
    
    print(f"Discovered {len(routes)} routes.")
    
    # Test GET endpoints where possible (without dynamic path params if not provided)
    # We will test a few common ones dynamically
    
    # Let's try to hit /api/v1 endpoints
    # 1. Admins
    print("Testing /api/v1/admins GET...")
    resp = client.get("/api/v1/admins")
    results["/api/v1/admins"] = {"status": resp.status_code, "body": resp.text[:100]}
    
    # 2. Parents
    print("Testing /api/v1/parents GET...")
    resp = client.get("/api/v1/parents")
    results["/api/v1/parents"] = {"status": resp.status_code, "body": resp.text[:100]}

    # 3. Drivers
    print("Testing /api/v1/drivers GET...")
    resp = client.get("/api/v1/drivers")
    results["/api/v1/drivers"] = {"status": resp.status_code, "body": resp.text[:100]}

    # 4. Students
    print("Testing /api/v1/students GET...")
    resp = client.get("/api/v1/students")
    results["/api/v1/students"] = {"status": resp.status_code, "body": resp.text[:100]}

    # 5. Buses
    print("Testing /api/v1/buses GET...")
    resp = client.get("/api/v1/buses")
    results["/api/v1/buses"] = {"status": resp.status_code, "body": resp.text[:100]}

    # 6. Routes
    print("Testing /api/v1/routes GET...")
    resp = client.get("/api/v1/routes")
    results["/api/v1/routes"] = {"status": resp.status_code, "body": resp.text[:100]}

    # 7. Dashboard Stats
    print("Testing /api/v1/dashboard/stats GET...")
    resp = client.get("/api/v1/dashboard/stats")
    results["/api/v1/dashboard/stats"] = {"status": resp.status_code, "body": resp.text[:500]}

    print("Test execution finished.")
    
    # Print results
    for endpoint, result in results.items():
        status = result["status"]
        if status >= 200 and status < 400:
            print(f"OK {endpoint} -> {status}")
        else:
            print(f"FAIL {endpoint} -> {status}")
            print(f"   Body: {result['body']}")
            
    # Check if there are any 500 errors
    errors = {k: v for k, v in results.items() if v["status"] >= 500}
    if errors:
        print(f"\nFound {len(errors)} endpoints with 500 errors.")
        sys.exit(1)
    else:
        print("\nAll tested GET endpoints responded without 500 server errors!")
        sys.exit(0)

if __name__ == "__main__":
    run_tests()
