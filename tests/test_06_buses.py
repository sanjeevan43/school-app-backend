import pytest
from fastapi.testclient import TestClient

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def mock_bus_data():
    return {
        "bus_id": "bus123",
        "registration_number": "TN38BZ1234",
        "seating_capacity": 40,
        "status": "ACTIVE",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

def test_create_bus(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_bus_data()
    payload = {
        "registration_number": "TN38BZ1234",
        "seating_capacity": 40
    }
    response = client.post("/api/v1/buses", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["bus_id"] == "bus123"

def test_get_buses(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [mock_bus_data()]
    response = client.get("/api/v1/buses", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["bus_id"] == "bus123"

def test_get_bus(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_bus_data()
    response = client.get("/api/v1/buses/bus123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["bus_id"] == "bus123"

def test_update_bus(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_bus_data()
    payload = {
        "seating_capacity": 50
    }
    response = client.put("/api/v1/buses/bus123", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["bus_id"] == "bus123"

def test_delete_bus(client: TestClient, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/buses/bus123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data.get("message", "").lower() or data == {"message": "Bus deleted successfully"}
