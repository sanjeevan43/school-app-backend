import requests
import json

BASE_URL = "http://localhost:8080/api/v1"
ADMIN_KEY = "selvagam-admin-key-2024"
HEADERS = {"x-admin-key": ADMIN_KEY}

def test_notification_logs():
    print("\n[1] Testing /admin-parent-notifications (no filters)")
    response = requests.get(f"{BASE_URL}/admin-parent-notifications", headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Count: {len(response.json())}")

    route_id = "3af62acb-491e-4dbc-b25f-fe0a8b35171f"
    print(f"\n[2] Testing /admin-parent-notifications?route_id={route_id}")
    response = requests.get(f"{BASE_URL}/admin-parent-notifications", params={"route_id": route_id}, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Count: {len(response.json())}")

    class_id = "02dc54f3-1977-4829-94f1-70549e09a031"
    print(f"\n[3] Testing /admin-parent-notifications?class_id={class_id}")
    response = requests.get(f"{BASE_URL}/admin-parent-notifications", params={"class_id": class_id}, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Count: {len(response.json())}")

    print(f"\n[4] Testing /admin-parent-notifications/route/{route_id}")
    response = requests.get(f"{BASE_URL}/admin-parent-notifications/route/{route_id}", headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Count: {len(response.json())}")

    print(f"\n[5] Testing /admin-parent-notifications/class/{class_id}")
    response = requests.get(f"{BASE_URL}/admin-parent-notifications/class/{class_id}", headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Count: {len(response.json())}")

if __name__ == "__main__":
    test_notification_logs()
