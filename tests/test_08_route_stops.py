import pytest
from fastapi.testclient import TestClient

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def mock_route_stop_data():
    return {
        "stop_id": "stop123",
        "route_id": "route123",
        "stop_name": "Stop 1",
        "location": "Location 1",
        "latitude": 10.0,
        "longitude": 20.0,
        "pickup_stop_order": 1,
        "drop_stop_order": 1,
        "created_at": "2023-01-01T00:00:00"
    }

def test_create_route_stop(client: TestClient, mock_db_cursor):
    # Mocking for the validations
    mock_db_cursor.fetchone.return_value = {"route_id": "route123", "max_pickup": 0, "max_drop": 0}
    # Mocking for the return statement (get_all_route_stops returns fetch_all)
    mock_db_cursor.fetchall.return_value = [mock_route_stop_data()]
    
    payload = {
        "route_id": "route123",
        "stop_name": "Stop 1",
        "pickup_stop_order": 1,
        "drop_stop_order": 1
    }
    response = client.post("/api/v1/route-stops", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["stop_id"] == "stop123"
    assert data[0]["stop_name"] == "Stop 1"

def test_get_route_stops(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [mock_route_stop_data()]
    response = client.get("/api/v1/route-stops", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["stop_id"] == "stop123"

def test_get_route_stop(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_route_stop_data()
    response = client.get("/api/v1/route-stops/stop123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["stop_id"] == "stop123"

def test_update_route_stop(client: TestClient, mock_db_cursor):
    # For PUT /route-stops/{stop_id}, it likely returns a single RouteStopResponse
    mock_db_cursor.fetchone.return_value = mock_route_stop_data()
    payload = {
        "stop_name": "Stop 1 Updated"
    }
    response = client.put("/api/v1/route-stops/stop123", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["stop_id"] == "stop123"

def test_delete_route_stop(client: TestClient, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/route-stops/stop123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "deleted" in data.get("message", "").lower()
