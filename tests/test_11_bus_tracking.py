import pytest
from fastapi import status
from unittest.mock import MagicMock

HEADERS = {"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"}

def test_update_bus_stop_progression(client, mocker):
    mock_update = mocker.patch("app.api.routes.bus_tracking_service.update_bus_location")
    # For asyncio methods, need an AsyncMock if it's awaited, but wait, is update_bus_location awaited? 
    # Yes, it's an async method in bus_tracking_service.
    from unittest.mock import AsyncMock
    mock_update_async = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.routes.bus_tracking_service.update_bus_location", new=mock_update_async)
    
    payload = {
        "trip_id": "test_trip_123",
        "latitude": 12.9716,
        "longitude": 77.5946
    }
    
    response = client.post("/api/v1/bus-tracking/stop-progression", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_send_custom_notification(client, mock_db_cursor, mocker):
    mock_db_cursor.fetchone.return_value = {
        "trip_id": "test_trip_123",
        "route_id": "test_route_123"
    }
    mock_db_cursor.fetchall.return_value = [{"student_id": "std1"}]
    
    mocker.patch("app.api.routes.bus_tracking_service.get_parent_tokens_for_students", return_value=["token1"])
    from unittest.mock import AsyncMock
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "trip_id": "test_trip_123",
        "message": "Bus is delayed by 10 minutes",
        "stop_id": "test_stop_123"
    }
    
    response = client.post("/api/v1/bus-tracking/notify", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_update_fcm_cache(client, mocker):
    mocker.patch("app.api.routes.bus_tracking_service.update_route_fcm_cache", return_value={"success": True})
    
    response = client.post("/api/v1/bus-tracking/cache-update/test_route_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_get_fcm_cache(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "route_id": "test_route_123",
        "stop_fcm_map": '{"stop1": ["token1"]}',
        "updated_at": "2024-01-01T00:00:00"
    }
    
    response = client.get("/api/v1/bus-tracking/cache/test_route_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
