import pytest
from fastapi import status
from unittest.mock import AsyncMock

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com",
    "x-admin-key": "test_admin_key"
}

def test_get_notifications_status(client):
    response = client.get("/api/v1/notifications/status", headers=HEADERS)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

def test_send_notification(client, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_topic", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body",
        "topic": "all_users",
        "message_type": "audio"
    }
    response = client.post("/api/v1/send-notification", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_send_device_notification(client, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body",
        "token": "token123",
        "recipient_type": "parent",
        "message_type": "audio"
    }
    response = client.post("/api/v1/notifications/send-device", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_broadcast_drivers(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_db_cursor.fetchall.return_value = [{"fcm_token": "token1"}]
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body",
        "message_type": "audio"
    }
    response = client.post("/api/v1/notifications/broadcast/drivers", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
