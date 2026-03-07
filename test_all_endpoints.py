import requests
import json

BASE_URL = "http://localhost:8080"
SCHEMA_URL = f"{BASE_URL}/openapi.json"
ADMIN_KEY = "selvagam-admin-key-2024"
HEADERS = {"x-admin-key": ADMIN_KEY}

def get_all_routes():
    try:
        response = requests.get(SCHEMA_URL)
        if response.status_code == 200:
            return response.json().get('paths', {})
    except Exception as e:
        print(f"Error fetching schema: {e}")
    return {}

def test_routes():
    paths = get_all_routes()
    if not paths:
        print("No routes found.")
        return

    results = []
    
    # Sensible defaults for path parameters (gathered from previous knowledge of the DB)
    defaults = {
        "student_id": "6e4c5102-20a6-413b-8ffc-7ad5d662f228",
        "parent_id": "7d92eafb-76eb-41ca-bc3b-633eb0afa71b",
        "route_id": "3af62acb-491e-4dbc-b25f-fe0a8b35171f",
        "class_id": "02dc54f3-1977-4829-94f1-70549e09a031",
        "trip_id": "6348b2c4-f060-4405-b56c-602460d7e543",
        "admin_id": "5081a93e-1533-4932-bf34-cd5b33a3606e",
        "bus_id": "1071a9cb-2789-4104-94b4-8b3d1f540ed8",
        "driver_id": "56bda442-ec90-4511-ae55-ce25b15a2b5a",
        "notification_id": "9e963a5e-2352-439d-b2c6-eb8081c80ecf",
        "location": "Saalur",
        "trip_type": "PICKUP"
    }

    print(f"{'METHOD':<8} {'PATH':<60} {'STATUS':<10} {'RESULT'}")
    print("-" * 100)

    for path, methods in paths.items():
        # Clean path for display
        display_path = path
        
        for method, info in methods.items():
            if method.lower() != 'get':
                continue # Only testing GET for now to avoid data mutation
            
            # Substitute path parameters
            test_path = path
            skip = False
            for param, value in defaults.items():
                if f"{{{param}}}" in test_path:
                    test_path = test_path.replace(f"{{{param}}}", value)
            
            # If there are still placeholders, skip
            if "{" in test_path:
                print(f"{method.upper():<8} {test_path:<60} SKIP       Placeholder missing")
                continue

            try:
                url = f"{BASE_URL}{test_path}"
                res = requests.get(url, headers=HEADERS, timeout=5)
                status = res.status_code
                summary = "OK" if status < 400 else "ERR"
                
                # Check for common error signatures in response
                error_detail = ""
                if status >= 400:
                    try:
                        error_detail = res.json().get('detail', res.text[:50])
                    except:
                        error_detail = res.text[:50]
                
                print(f"{method.upper():<8} {test_path:<60} {status:<10} {summary} {error_detail}")
                results.append({"path": path, "method": method, "status": status, "error": error_detail})
            except Exception as e:
                print(f"{method.upper():<8} {test_path:<60} EXCP       {str(e)[:50]}")

if __name__ == "__main__":
    test_routes()
