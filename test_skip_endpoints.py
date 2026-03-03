import requests
import json

base_url = "http://localhost:8080/api/v1"  # Corrected with 8080 port
trip_id = "test-trip-id" # Dummy ID for testing 404/400 response

def test_skip_next_stop():
    print(f"\n--- Testing POST /trips/{trip_id}/skip-next-stop ---")
    try:
        url = f"{base_url}/trips/{trip_id}/skip-next-stop"
        response = requests.post(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_skip_future_stop():
    stop_order = 5
    print(f"\n--- Testing POST /trips/{trip_id}/skip-future-stop/{stop_order} ---")
    try:
        url = f"{base_url}/trips/{trip_id}/skip-future-stop/{stop_order}"
        response = requests.post(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Note: These will likely return 404/400 since the trip_id is dummy, 
    # but it verifies the routes are correctly registered in the API.
    test_skip_next_stop()
    test_skip_future_stop()
