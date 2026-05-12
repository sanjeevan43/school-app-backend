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

def verify_automatic_password_logic():
    print("--- Final Verification: Automatic Password Logic Refresh ---")
    
    # 1. Create Test Admin
    # Logic: Name(4) + @ + Phone(last 4)
    phone_v1 = 9000001111
    name_v1 = "Sanjeev"
    expected_pass_v1 = "Sanj@1111"
    
    print(f"Step 1: Creating admin {name_v1} with phone {phone_v1}...")
    create_resp = client.post("/api/v1/admins", json={
        "name": name_v1,
        "phone": phone_v1,
        "email": "sanjeev@example.com"
    }, headers=HEADERS)
    
    admin_id = create_resp.json()["admin_id"]
    
    # Verify login v1
    print(f"Verifying login with {expected_pass_v1}...")
    login_v1 = client.post("/api/v1/auth/admin/login", json={"phone": phone_v1, "password": expected_pass_v1})
    if login_v1.status_code == 200:
        print("SUCCESS: Login v1 worked.")
    else:
        print(f"FAILURE: Login v1 failed: {login_v1.text}")

    # 2. Update Phone Number
    phone_v2 = 9000002222
    expected_pass_v2 = "Sanj@2222" # Should update automatically!
    
    print(f"Step 2: Updating phone to {phone_v2}...")
    update_resp = client.put(f"/api/v1/admins/{admin_id}", json={
        "phone": phone_v2
    }, headers=HEADERS)
    
    if update_resp.status_code != 200:
        print(f"Update failed: {update_resp.text}")
        return

    # 3. Verify login v2 with NEW default password
    print(f"Step 3: Attempting login with NEW phone {phone_v2} and expected NEW password {expected_pass_v2}...")
    login_v2 = client.post("/api/v1/auth/admin/login", json={"phone": phone_v2, "password": expected_pass_v2})
    
    if login_v2.status_code == 200:
        print("SUCCESS: Automatic Password logic successfully applied and verified!")
    else:
        print(f"FAILURE: System is still expecting the old password or hash is corrupted: {login_v2.text}")

    # Cleanup
    execute_query("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
    print("\nCleanup Complete.")

if __name__ == "__main__":
    verify_automatic_password_logic()
