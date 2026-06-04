import pytest
from fastapi.testclient import TestClient

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def mock_route_data():
    return {
        "route_id": "route123",
        "name": "Route 1",
        "routes_active_status": "ACTIVE",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

def test_create_route(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_route_data()
    payload = {
        "name": "Route 1"
    }
    response = client.post("/api/v1/routes", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["route_id"] == "route123"
    assert data["name"] == "Route 1"

def test_get_routes(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [mock_route_data()]
    response = client.get("/api/v1/routes", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["route_id"] == "route123"

def test_get_route(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_route_data()
    response = client.get("/api/v1/routes/route123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["route_id"] == "route123"

def test_update_route(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_route_data()
    payload = {
        "name": "Route 1 Updated"
    }
    response = client.put("/api/v1/routes/route123", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["route_id"] == "route123"

def test_delete_route(client: TestClient, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/routes/route123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data.get("message", "").lower() or "deleted" in data.get("message", "").lower()
