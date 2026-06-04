import pytest
from fastapi import status
from unittest.mock import MagicMock

HEADERS = {"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"}

def test_create_trip(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "trip_id": "test_trip_123",
        "bus_id": "test_bus_123",
        "driver_id": "test_driver_123",
        "route_id": "test_route_123",
        "trip_date": "2024-01-01",
        "trip_type": "PICKUP",
        "status": "NOT_STARTED",
        "current_stop_order": 0,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    
    trip_data = {
        "bus_id": "test_bus_123",
        "driver_id": "test_driver_123",
        "route_id": "test_route_123",
        "trip_date": "2024-01-01",
        "trip_type": "PICKUP"
    }
    
    response = client.post("/api/v1/trips", json=trip_data, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["trip_id"] == "test_trip_123"

def test_get_all_trips(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {
            "trip_id": "test_trip_123",
            "bus_id": "test_bus_123",
            "driver_id": "test_driver_123",
            "route_id": "test_route_123",
            "trip_date": "2024-01-01",
            "trip_type": "PICKUP",
            "status": "NOT_STARTED",
            "current_stop_order": 0,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    ]
    
    response = client.get("/api/v1/trips", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_trip(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "trip_id": "test_trip_123",
        "bus_id": "test_bus_123",
        "driver_id": "test_driver_123",
        "route_id": "test_route_123",
        "trip_date": "2024-01-01",
        "trip_type": "PICKUP",
        "status": "NOT_STARTED",
        "current_stop_order": 0,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    
    response = client.get("/api/v1/trips/test_trip_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["trip_id"] == "test_trip_123"

def test_get_ongoing_trips(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {
            "trip_id": "test_trip_123",
            "bus_id": "test_bus_123",
            "driver_id": "test_driver_123",
            "route_id": "test_route_123",
            "trip_date": "2024-01-01",
            "trip_type": "PICKUP",
            "status": "ONGOING",
            "current_stop_order": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    ]
    
    response = client.get("/api/v1/trips/ongoing/all", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_update_trip(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "trip_id": "test_trip_123",
        "bus_id": "test_bus_123",
        "driver_id": "test_driver_123",
        "route_id": "test_route_123",
        "trip_date": "2024-01-01",
        "trip_type": "PICKUP",
        "status": "ONGOING",
        "current_stop_order": 2,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1
    
    trip_update = {
        "status": "ONGOING",
        "current_stop_order": 2
    }
    
    response = client.put("/api/v1/trips/test_trip_123", json=trip_update, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["current_stop_order"] == 2

def test_delete_trip(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    
    response = client.delete("/api/v1/trips/test_trip_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Trip deleted successfully"
