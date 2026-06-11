import pytest
from fastapi import status
from unittest.mock import AsyncMock, MagicMock
from app.services.proximity_service import proximity_service

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com",
    "x-admin-key": "test_admin_key"
}

def test_bus_tracking_location_endpoint(client, mocker):
    # Mock the services called by the combined endpoint
    mock_update_bus = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.bus_tracking_service.update_bus_location", new=mock_update_bus)
    
    mock_proximity = AsyncMock(return_value={
        "success": True, 
        "trip_id": "test_trip_123", 
        "current_order": 1,
        "notifications_sent": []
    })
    mocker.patch("app.api.notification_routes.proximity_service.process_location_update", new=mock_proximity)
    
    payload = {
        "trip_id": "test_trip_123",
        "latitude": 13.0827,
        "longitude": 80.2707
    }
    
    response = client.post("/api/v1/bus-tracking/location", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["trip_id"] == "test_trip_123"
    assert "proximity_alerts" in data
    assert "stop_progression" in data

def test_trip_start_endpoint(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    
    # Mock trip lookup in DB
    mock_db_cursor.fetchone.return_value = {"route_id": "test_route_123", "trip_type": "PICKUP"}
    
    # Mock proximity_service.start_trip
    mock_start_trip = AsyncMock(return_value={"success": True, "recipients": 5})
    mocker.patch("app.api.notification_routes.proximity_service.start_trip", new=mock_start_trip)
    
    response = client.post("/api/v1/trip/start?trip_id=test_trip_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["recipients"] == 5

def test_trip_complete_endpoint(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    
    # Mock trip lookup in DB
    mock_db_cursor.fetchone.return_value = {"route_id": "test_route_123", "trip_type": "PICKUP"}
    
    # Mock proximity_service.complete_trip
    mock_complete_trip = AsyncMock(return_value={"success": True, "recipients": 5, "trip_type": "PICKUP"})
    mocker.patch("app.api.notification_routes.proximity_service.complete_trip", new=mock_complete_trip)
    
    response = client.post("/api/v1/trip/complete?trip_id=test_trip_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["recipients"] == 5

@pytest.mark.asyncio
async def test_proximity_service_methods(mocker):
    # Mock database functions inside proximity_service module
    mock_execute = MagicMock()
    mocker.patch("app.services.proximity_service.execute_query", mock_execute)
    
    # Mock FCM tokens call
    mocker.patch("app.services.proximity_service.notification_service.broadcast_to_tokens", new=AsyncMock(return_value={"success": True}))
    
    # Test fetch_tokens_by_route
    mock_execute.return_value = [{"fcm_token": "token1"}, {"fcm_token": "token2"}]
    tokens = await proximity_service.fetch_tokens_by_route("route_123")
    assert tokens == ["token1", "token2"]
    
    # Test fetch_route_stops
    mock_execute.return_value = [
        {"stop_id": "stop1", "stop_name": "Stop 1", "latitude": 13.0, "longitude": 80.0, "stop_order": 1}
    ]
    stops = await proximity_service.fetch_route_stops("route_123", "PICKUP")
    assert len(stops) == 1
    assert stops[0]["stop_name"] == "Stop 1"
    
    # Test process_location_update
    # Configure mock_execute to return trip info on first call and stop list info on subsequent calls or similar
    def side_effect(query, params=None, fetch_one=False, fetch_all=False):
        if "trips" in query:
            return {"current_stop_order": 1, "route_id": "route_123", "trip_type": "PICKUP"}
        if "route_stops" in query:
            return [
                {"stop_id": "stop1", "stop_name": "Stop 1", "latitude": 13.0, "longitude": 80.0, "stop_order": 1}
            ]
        return None
        
    mock_execute.side_effect = side_effect
    res = await proximity_service.process_location_update("trip_123", 13.001, 80.001)
    assert res["success"] is True
    assert res["trip_id"] == "trip_123"
    assert res["current_order"] == 1
