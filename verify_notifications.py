import requests
import json

BASE_URL = "http://localhost:8080/api/v1"
ADMIN_KEY = "selvagam-admin-key-2024"
HEADERS = {"x-admin-key": ADMIN_KEY}

# Test IDs from DB
STUDENT_ID = "0314b008-ebdd-47f6-9ed2-b02df532e8d0"
ROUTE_ID = "a9440a08-ec23-4bd6-8bc4-bb1f5522546d"
CLASS_ID = "02dc54f3-1977-4829-94f1-70549e09a031"
PARENT_ID = "7d92eafb-76eb-41ca-bc3b-633eb0afa71b"

def test_endpoint(name, url, method="GET", data=None):
    print(f"\n--- Testing {name} ---")
    print(f"URL: {url}")
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        else:
            response = requests.post(url, json=data, headers=HEADERS)
        
        print(f"Status: {response.status_code}")
        if response.status_code < 300:
            res_data = response.json()
            if isinstance(res_data, list):
                print(f"Count: {len(res_data)}")
                if len(res_data) > 0:
                    print(f"Sample Notification: {res_data[0].get('title')} - {res_data[0].get('recipient_type', 'N/A')}")
            else:
                print(f"Response: {res_data.get('notification_id', res_data)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def run_tests():
    # 1. Create a Test Notification (Student)
    print("\n--- Test 1: Create Student Notification ---")
    payload = {
        "title": "Student Alert",
        "message": "Direct message to student parents",
        "recipient_type": "STUDENT",
        "student_id": STUDENT_ID,
        "sent_by_admin_id": ADMIN_ID
    }
    test_endpoint("Create Student Notification", f"{BASE_URL}/admin-parent-notifications", "POST", payload)

    # 1b. Create a Route Notification
    print("\n--- Test 1b: Create Route Notification ---")
    payload_route = {
        "title": "Route Alert",
        "message": "Message to all on this route",
        "recipient_type": "ROUTE",
        "route_id": ROUTE_ID,
        "sent_by_admin_id": ADMIN_ID
    }
    test_endpoint("Create Route Notification", f"{BASE_URL}/admin-parent-notifications", "POST", payload_route)

    # 2. Get All
    test_endpoint("All Notifications", f"{BASE_URL}/admin-parent-notifications?limit=5")

    # 3. Get by Student
    test_endpoint("By Student", f"{BASE_URL}/admin-parent-notifications/student/{STUDENT_ID}")

    # 4. Get by Route
    test_endpoint("By Route", f"{BASE_URL}/admin-parent-notifications/route/{ROUTE_ID}")

    # 5. Get by Class
    test_endpoint("By Class", f"{BASE_URL}/admin-parent-notifications/class/{CLASS_ID}")

    # 7. Test Admin Broadcast (Now also logs)
    # Note: This might take time because it tries to send FCM. 
    # But let's check it for logging.
    broadcast_payload = {
        "title": "Global Test",
        "body": "Global broadcast message with logging",
        "messageType": "audio"
    }
    test_endpoint("Global Broadcast (Logging Test)", f"{BASE_URL}/notifications/broadcast/parents", "POST", broadcast_payload)

if __name__ == "__main__":
    run_tests()
