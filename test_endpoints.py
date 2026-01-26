from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

endpoints = [
    "GET /",
    "GET /health", 
    "GET /api/v1/admins",
    "GET /api/v1/parents",
    "GET /api/v1/drivers",
    "GET /api/v1/routes",
    "GET /api/v1/buses",
    "GET /api/v1/students",
    "GET /api/v1/trips"
]

for endpoint in endpoints:
    method, path = endpoint.split(" ", 1)
    try:
        if method == "GET":
            response = client.get(path)
        print(f"{endpoint}: {response.status_code}")
        if response.status_code == 500:
            print(f"  Error: {response.text[:200]}")
    except Exception as e:
        print(f"{endpoint}: EXCEPTION - {e}")