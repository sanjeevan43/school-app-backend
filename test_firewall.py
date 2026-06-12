import os
os.environ["DEBUG"] = "False"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("--- Test 1: Direct Browser Access (Swagger Docs) ---")
response = client.get("/docs", headers={"User-Agent": "Mozilla/5.0 Windows NT 10.0"})
print(f"Status: {response.status_code}")
if response.status_code == 403:
    print(f"Response: {response.json()}")
else:
    print("FAILED! Should be 403")

print("\n--- Test 2: Direct Browser Access (API Endpoint) ---")
response = client.get("/", headers={"User-Agent": "Mozilla/5.0 Safari"})
print(f"Status: {response.status_code}")
if response.status_code == 403:
    print(f"Response: {response.json()}")
else:
    print("FAILED! Should be 403")

print("\n--- Test 3: Authorized Website Access ---")
response = client.get("/", headers={"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("Success: 200 OK")
else:
    print("FAILED! Should be 200")

print("\n--- Test 4: Mobile App Access (Non-Browser User-Agent) ---")
response = client.get("/", headers={"User-Agent": "Dart/2.19 (dart:io)"})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("Success: 200 OK")
else:
    print("FAILED! Should be 200")

print("\n--- Test 5: Unauthorized Website Access ---")
response = client.get("/", headers={"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://evil.com"})
print(f"Status: {response.status_code}")
if response.status_code == 403:
    print(f"Response: {response.json()}")
else:
    print("FAILED! Should be 403")
