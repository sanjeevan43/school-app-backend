import requests
import json

base_url = "http://127.0.0.1:8080"
endpoints = [
    "/api/v1/parents",
    "/api/v1/drivers",
    "/api/v1/students",
    "/api/v1/routes",
    "/api/v1/buses",
    "/api/v1/classes",
    "/api/v1/dashboard/summary",
    "/api/notifications/status"
]

results = {}

print("Scanning for 500 errors on 127.0.0.1:8080...")
for ep in endpoints:
    try:
        url = base_url + ep
        resp = requests.get(url, timeout=10)
        print(f"{resp.status_code} at {ep}")
        if resp.status_code == 500:
            results[ep] = resp.json()
    except Exception as e:
        print(f"Error at {ep}: {e}")

with open('scanner_results.json', 'w') as f:
    json.dump(results, f, indent=2)
