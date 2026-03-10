import requests
import json
import uuid

BASE_URL = "http://localhost:8080/api/v1"
ADMIN_KEY = "selvagam-admin-key-2024"
HEADERS = {"x-admin-key": ADMIN_KEY}

def print_result(name, response):
    status = response.status_code
    summary = "PASS" if status < 400 else "FAIL"
    print(f"[{summary}] {name:<40} | Status: {status}")
    if status >= 400:
        try:
            print(f"      Error: {response.json().get('detail', response.text[:100])}")
        except:
            print(f"      Error: {response.text[:100]}")

def test_a_to_z():
    print("=== School Transport Management API: A to Z Verification ===\n")

    # 1. System Health & Docs
    try:
        health = requests.get("http://localhost:8080/health")
        print_result("System Health Check", health)
    except:
        print("[FAIL] System Health Check | Connection Refused")

    # 2. Authentication / Profiles
    # Note: Using a phone number that might exist or just checking the endpoint exists
    print_result("Admins List", requests.get(f"{BASE_URL}/admins", headers=HEADERS))
    
    # 3. Parents
    print_result("Parents List", requests.get(f"{BASE_URL}/parents", headers=HEADERS))
    print_result("Parent FCM Tokens", requests.get(f"{BASE_URL}/parents/fcm-tokens/all", headers=HEADERS))

    # 4. Drivers
    print_result("Drivers List", requests.get(f"{BASE_URL}/drivers", headers=HEADERS))
    print_result("Driver FCM Tokens", requests.get(f"{BASE_URL}/drivers/fcm-tokens/all", headers=HEADERS))

    # 5. Buses
    print_result("Buses List", requests.get(f"{BASE_URL}/buses", headers=HEADERS))

    # 6. Routes
    print_result("Routes List", requests.get(f"{BASE_URL}/routes", headers=HEADERS))

    # 7. Students
    print_result("Students List", requests.get(f"{BASE_URL}/students", headers=HEADERS))

    # 8. Trips
    print_result("Ongoing Trips", requests.get(f"{BASE_URL}/trips/ongoing/all", headers=HEADERS))

    # 9. Notifications
    print_result("Notification Service Status", requests.get(f"{BASE_URL}/notifications/status", headers=HEADERS))

    # 10. NEW FEATURES (Verification of recent work)
    print("\n--- Verifying Recent Features ---")
    
    # Test Logout Endpoint
    test_token = "verify-token-" + str(uuid.uuid4())
    requests.post(f"{BASE_URL}/fcm-tokens", json={"fcm_token": test_token, "parent_id": "7d92eafb-76eb-41ca-bc3b-633eb0afa71b"}, headers=HEADERS)
    logout_res = requests.post(f"{BASE_URL}/auth/logout", json={"fcm_token": test_token})
    print_result("New Logout Endpoint", logout_res)
    
    # Test Force Logout Logic (Parent)
    parent_id = "7d92eafb-76eb-41ca-bc3b-633eb0afa71b"
    new_token = "verify-new-token-" + str(uuid.uuid4())
    login_res = requests.put(f"{BASE_URL}/parents/{parent_id}/fcm-token", json={"fcm_token": new_token}, headers=HEADERS)
    print_result("Single Device login (Parent)", login_res)

    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    test_a_to_z()
