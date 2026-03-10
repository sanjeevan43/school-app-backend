import requests
import json
import uuid

BASE_URL = "http://localhost:8080/api/v1"
ADMIN_KEY = "selvagam-admin-key-2024"
HEADERS = {"x-admin-key": ADMIN_KEY}

def test_logout():
    print("\n--- Testing Logout ---")
    test_token = "test-token-" + str(uuid.uuid4())
    
    # 1. Register a token first via endpoint
    print(f"Registering test token: {test_token}")
    reg_payload = {
        "fcm_token": test_token,
        "parent_id": "7d92eafb-76eb-41ca-bc3b-633eb0afa71b"
    }
    requests.post(f"{BASE_URL}/fcm-tokens", json=reg_payload, headers=HEADERS)
    
    # 2. Test logout
    logout_payload = {"fcm_token": test_token}
    response = requests.post(f"{BASE_URL}/auth/logout", json=logout_payload)
    print(f"Logout Response: {response.status_code} - {response.json()}")
    
    # 3. Verify it was deleted (check all parent tokens)
    verify_res = requests.get(f"{BASE_URL}/parents/fcm-tokens/all", headers=HEADERS)
    tokens_res = verify_res.json()
    tokens = tokens_res.get('fcm_tokens', [])
    if test_token in tokens:
        print("FAILED: Token still exists after logout")
    else:
        print("SUCCESS: Token removed after logout")

def test_parent_single_device_login():
    print("\n--- Testing Parent Single Device Login ---")
    parent_id = "7d92eafb-76eb-41ca-bc3b-633eb0afa71b"
    token_1 = "token-device-1-" + str(uuid.uuid4())
    token_2 = "token-device-2-" + str(uuid.uuid4())
    
    # 1. Login Device 1
    print(f"Registering Device 1 (Token: {token_1})")
    requests.put(f"{BASE_URL}/parents/{parent_id}/fcm-token", json={"fcm_token": token_1}, headers=HEADERS)
    
    # 2. Login Device 2 (Should trigger force logout for Device 1)
    print(f"Registering Device 2 (Token: {token_2})")
    response = requests.put(f"{BASE_URL}/parents/{parent_id}/fcm-token", json={"fcm_token": token_2}, headers=HEADERS)
    print(f"Response: {response.status_code} - {response.json()}")
    
    # 3. Verify only Device 2 is in the system
    verify_res = requests.get(f"{BASE_URL}/parents/fcm-tokens/all", headers=HEADERS)
    tokens_data = verify_res.json()
    tokens = tokens_data.get('fcm_tokens', [])
    print(f"Tokens in system for parent {parent_id}: {tokens}")
    
    if token_1 not in tokens and token_2 in tokens:
        print("SUCCESS: Device 1 removed, Device 2 registered")
    else:
        print(f"FAILED: Expected only Token 2. Got: {tokens}")

def test_driver_single_device_login():
    print("\n--- Testing Driver Single Device Login ---")
    driver_id = "56bda442-ec90-4511-ae55-ce25b15a2b5a"
    token_1 = "driver-token-1-" + str(uuid.uuid4())
    token_2 = "driver-token-2-" + str(uuid.uuid4())
    
    # 1. Login Device 1
    print(f"Registering Driver Device 1 (Token: {token_1})")
    requests.patch(f"{BASE_URL}/drivers/{driver_id}/fcm-token", json={"fcm_token": token_1}, headers=HEADERS)
    
    # 2. Login Device 2
    print(f"Registering Driver Device 2 (Token: {token_2})")
    response = requests.patch(f"{BASE_URL}/drivers/{driver_id}/fcm-token", json={"fcm_token": token_2}, headers=HEADERS)
    print(f"Response: {response.status_code} - {response.json()}")
    
    # 3. Verify Driver has Token 2
    driver_res = requests.get(f"{BASE_URL}/drivers/{driver_id}", headers=HEADERS)
    current_token = driver_res.json().get('fcm_token')
    print(f"Current Driver Token: {current_token}")
    
    if current_token == token_2:
        print("SUCCESS: Driver token updated to Token 2")
    else:
        print(f"FAILED: Driver token is {current_token}, expected {token_2}")

if __name__ == "__main__":
    try:
        test_logout()
        test_parent_single_device_login()
        test_driver_single_device_login()
    except Exception as e:
        print(f"Test failed with error: {e}")
