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

def test_broadcast_parents(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    # Mock system admin lookup
    mock_db_cursor.fetchone.return_value = {"admin_id": "admin_123"}
    # Mock parent tokens lookup
    mock_db_cursor.fetchall.return_value = [{"fcm_token": "token1"}]
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body",
        "messageType": "audio"
    }
    response = client.post("/api/v1/notifications/broadcast/parents", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_send_student_notification(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_db_cursor.fetchone.return_value = {"admin_id": "admin_123"}
    mock_db_cursor.fetchall.return_value = [{"fcm_token": "token1"}]
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body"
    }
    response = client.post("/api/v1/notifications/student/std123", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_send_parent_notification_direct(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_db_cursor.fetchone.return_value = {"admin_id": "admin_123"}
    mock_db_cursor.fetchall.return_value = [{"fcm_token": "token1"}]
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body"
    }
    response = client.post("/api/v1/notifications/parent/p123", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_send_route_notification(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_db_cursor.fetchone.return_value = {"admin_id": "admin_123"}
    mock_db_cursor.fetchall.return_value = [{"fcm_token": "token1"}]
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body"
    }
    response = client.post("/api/v1/notifications/route/route123", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_send_class_notification(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_db_cursor.fetchone.return_value = {"admin_id": "admin_123"}
    mock_db_cursor.fetchall.return_value = [{"fcm_token": "token1"}]
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body"
    }
    response = client.post("/api/v1/notifications/class/class123", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_send_location_notification(client, mock_db_cursor, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_db_cursor.fetchone.return_value = {"admin_id": "admin_123"}
    mock_db_cursor.fetchall.return_value = [{"fcm_token": "token1"}]
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.send_to_device", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "body": "Test Body",
        "route_id": "route123"
    }
    response = client.post("/api/v1/notifications/location/Loc123", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_manual_send(client, mocker):
    mocker.patch("app.api.notification_routes.ADMIN_KEY", "test_admin_key")
    mock_send = AsyncMock(return_value={"success": True})
    mocker.patch("app.api.notification_routes.notification_service.broadcast_to_tokens", new=mock_send)
    
    payload = {
        "title": "Test Title",
        "message": "Test Body",
        "tokens": ["token1"]
    }
    response = client.post("/api/v1/notifications/manual-send", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

