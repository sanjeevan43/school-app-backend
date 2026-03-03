import requests
import json
base_url = "http://localhost:8080/api/v1"
trip_id = "f67002e4-b9c0-42ad-ad83-1adacfa70933"
res = requests.get(f"{base_url}/trips/{trip_id}")
print(f"Status: {res.status_code}")
print(f"Headers: {dict(res.headers)}")
print(f"JSON: {json.dumps(res.json(), indent=2)}")
