import pytest
from fastapi import status
from unittest.mock import AsyncMock, MagicMock

HEADERS = {"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"}

def test_start_trip_route_endpoint(client, mock_db_cursor, mocker):
    # Mock database responses for start_trip
    # 1. Update query row count
    # 2. get_trip select query
    # 3. get_students_for_route_stop select query
    # 4. get_parent_tokens_for_students select query
    
    call_count = 0
    def mock_fetchone_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # First fetchone inside get_trip
            return {
                "trip_id": "test_trip_123",
                "route_id": "test_route_123",
                "trip_type": "PICKUP",
                "status": "ONGOING",
                "bus_id": "test_bus_123",
                "driver_id": "test_driver_123",
                "current_stop_order": 0,
                "is_first_stop_notified": 0,
                "skipped_stops": "[]",
                "stop_logs": "{}",
                "trip_date": "2024-01-01",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        return None

    mock_db_cursor.fetchone.side_effect = mock_fetchone_side_effect
    mock_db_cursor.rowcount = 1
    
    # Mock students and parent tokens
    mock_db_cursor.fetchall.return_value = [
        {"student_id": "student1", "name": "John", "fcm_token": "token1", "stop_name": "Stop 1", "location": "Loc 1"}
    ]
    
    # Mock proximity_service.start_trip
    mock_start = AsyncMock(return_value={"success": True, "recipients": 1})
    mocker.patch("app.services.proximity_service.proximity_service.start_trip", new=mock_start)
    
    # Mock notification_service.send_to_device
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.routes.notification_service.send_to_device", new=mock_send)
    
    response = client.put("/api/v1/trips/test_trip_123/start", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["trip_id"] == "test_trip_123"

def test_update_driver_location_endpoint(client, mock_db_cursor):
    # Check driver exists query
    mock_db_cursor.fetchone.return_value = {"driver_id": "driver_123"}
    mock_db_cursor.rowcount = 1
    
    payload = {
        "latitude": 13.0827,
        "longitude": 80.2707
    }
    
    response = client.put("/api/v1/drivers/driver_123/location", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Location updated successfully"

def test_skip_next_stop_endpoint(client, mocker):
    mock_skip = AsyncMock(return_value={"success": True, "message": "Stop skipped"})
    mocker.patch("app.api.routes.bus_tracking_service.skip_stop", new=mock_skip)
    
    response = client.post("/api/v1/trips/test_trip_123/skip-next-stop", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

def test_skip_future_stop_endpoint(client, mocker):
    mock_skip = AsyncMock(return_value={"success": True, "message": "Stop skipped"})
    mocker.patch("app.api.routes.bus_tracking_service.skip_specific_stop", new=mock_skip)
    
    response = client.post("/api/v1/trips/test_trip_123/skip-future-stop/2", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

def test_update_trip_status_endpoint(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    mock_db_cursor.fetchone.return_value = {
        "trip_id": "test_trip_123",
        "status": "COMPLETED",
        "bus_id": "test_bus_123",
        "driver_id": "test_driver_123",
        "route_id": "test_route_123",
        "trip_date": "2024-01-01",
        "trip_type": "PICKUP",
        "current_stop_order": 0,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    
    payload = {
        "status": "COMPLETED"
    }
    
    response = client.put("/api/v1/trips/test_trip_123/status", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "COMPLETED"
