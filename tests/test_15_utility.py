import pytest
from fastapi import status

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def test_get_dashboard_summary(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "admins": 5,
        "parents": 100,
        "drivers": 20,
        "buses": 15,
        "routes": 10,
        "students": 150,
        "ongoing_trips": 2
    }
    response = client.get("/api/v1/dashboard/summary", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["admins"] == 5
    assert data["ongoing_trips"] == 2

def test_get_dashboard_stats(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "total_students": 150,
        "total_drivers": 20,
        "total_parents": 100,
        "total_routes": 10,
        "active": 10,
        "inactive": 5,
        "maintenance": 0,
        "spare": 0,
        "total_buses": 15,
        "expired_licenses": 0,
        "upcoming_fc": 0,
        "expired_insurance": 0
    }
    mock_db_cursor.fetchall.return_value = [
        {
            "route_id": "route1",
            "route_name": "Route 1",
            "male": 10,
            "female": 10,
            "total": 20
        }
    ]
    response = client.get("/api/v1/dashboard/stats", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "data" in data

def test_error_handling_dummy(client, mock_db_cursor):
    """
    GET /api/v1/error-handling returns List[ErrorHandlingResponse].
    ErrorHandlingResponse requires: error_id (str), created_at (datetime).
    Providing correct mock data so Pydantic serialisation succeeds → 200.
    """
    mock_db_cursor.fetchall.return_value = [
        {
            "error_id": "err-001",
            "error_type": "DB_ERROR",
            "error_code": 500,
            "error_description": "Test error",
            "created_at": "2023-01-01T00:00:00"
        }
    ]
    response = client.get("/api/v1/error-handling", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["error_id"] == "err-001"
