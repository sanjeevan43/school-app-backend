from fastapi.testclient import TestClient
import sys
import json

# Add backend to path
sys.path.insert(0, r"c:\HS\school_app\school-app-backend")
from main import app
from app.core.database import execute_query

client = TestClient(app)
ADMIN_KEY = "selvagam-admin-key-2024"
HEADERS = {"x-admin-key": ADMIN_KEY}

def test_parent_logic():
    print("--- Parent Password Refresh Test ---")
    
    # 1. Create Parent
    phone_v1 = 9000012345
    name_v1 = "Sanjeev"
    expected_pass_v1 = "Sanj@2345"
    
    print(f"Step 1: Creating parent {name_v1} with phone {phone_v1}...")
    create_resp = client.post("/api/v1/parents", json={
        "name": name_v1,
        "phone": phone_v1,
        "email": "parent_test@example.com",
        "parent_role": "FATHER"
    }, headers=HEADERS)
    
    if create_resp.status_code != 200:
        print(f"Create failed: {create_resp.text}")
        return

    parent_id = create_resp.json()["parent_id"]
    
    # Verify login v1
    print(f"Verifying login with {expected_pass_v1}...")
    login_v1 = client.post("/api/v1/auth/parent/login", json={"phone": phone_v1, "password": expected_pass_v1})
    if login_v1.status_code == 200:
        print("SUCCESS: Initial login worked.")
    else:
        print(f"FAILURE: Initial login failed: {login_v1.text}")

    # 2. Update Parent Details (Name and Phone)
    name_v2 = "Sanjeevan"
    phone_v2 = 9000067890
    expected_pass_v2 = "Sanj@7890" # First 4 of Sanjeevan + @ + last 4 of phone
    
    print(f"Step 2: Updating parent to {name_v2} and phone {phone_v2}...")
    update_resp = client.put(f"/api/v1/parents/{parent_id}", json={
        "name": name_v2,
        "phone": phone_v2
    }, headers=HEADERS)
    
    if update_resp.status_code != 200:
        print(f"Update failed: {update_resp.status_code} - {update_resp.text}")
        return

    # 3. Verify login v2
    print(f"Step 3: Attempting login with NEW phone {phone_v2} and NEW password {expected_pass_v2}...")
    login_v2 = client.post("/api/v1/auth/parent/login", json={"phone": phone_v2, "password": expected_pass_v2})
    
    if login_v2.status_code == 200:
        print("SUCCESS: Parent update and automatic password refresh verified!")
    else:
        print(f"FAILURE: Login failed after update: {login_v2.status_code} - {login_v2.text}")

    # Cleanup
    execute_query("DELETE FROM parents WHERE parent_id = %s", (parent_id,))
    print("\nCleanup Complete.")

if __name__ == "__main__":
    test_parent_logic()
