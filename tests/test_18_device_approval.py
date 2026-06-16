import pytest
from fastapi import status
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

HEADERS = {"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"}

def test_parent_direct_login(client, mock_db_cursor, mocker):
    """If no active FCM token exists, parent login returns access token directly."""
    # 1. Select parent
    # 2. Select fcm_token (returns None/empty)
    # 3. Update last login
    # 4. Insert/update fcm_token
    # 5. Fetch updated token info
    mocker.patch("app.api.notification_routes.verify_password", return_value=True)
    
    call_count = 0
    def mock_fetchone_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "parent_id": "parent_123",
                "phone": 9876543210,
                "password_hash": "hashed_pass",
                "name": "John Doe"
            }
        elif call_count == 2:
            return None # No active FCM token in DB
        return None

    mock_db_cursor.fetchone.side_effect = mock_fetchone_side_effect
    
    payload = {
        "phone": 9876543210,
        "password": "correct_password",
        "fcm_token": "new_fcm_token_123",
        "device_info": "Pixel 8"
    }
    
    response = client.post("/api/v1/auth/parent/login", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_parent_multi_device_login_pending(client, mock_db_cursor, mocker):
    """If different FCM token exists, login returns waiting_for_approval and no access token."""
    mocker.patch("app.api.notification_routes.verify_password", return_value=True)
    mocker.patch("app.api.routes.ensure_login_requests_columns")
    
    call_count = 0
    def mock_fetchone_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "parent_id": "parent_123",
                "phone": 9876543210,
                "password_hash": "hashed_pass",
                "name": "John Doe"
            }
        elif call_count == 2:
            return {"fcm_token": "old_fcm_token_abc"} # Active session exists!
        return None

    mock_db_cursor.fetchone.side_effect = mock_fetchone_side_effect
    
    payload = {
        "phone": 9876543210,
        "password": "correct_password",
        "fcm_token": "new_fcm_token_123",
        "device_info": "Pixel 8"
    }
    
    response = client.post("/api/v1/auth/parent/login", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    assert data["status"] == "waiting_for_approval"
    assert "request_id" in data
    assert "access_token" not in data


def test_get_login_request_status_pending(client, mock_db_cursor, mocker):
    """Status endpoint returns PENDING and no token while waiting."""
    mocker.patch("app.api.routes.ensure_login_requests_columns")
    
    mock_db_cursor.fetchone.return_value = {
        "request_id": "req_123",
        "user_id": "parent_123",
        "user_type": "parent",
        "status": "PENDING",
        "expires_at": datetime.now() + timedelta(minutes=5)
    }
    
    response = client.get("/api/v1/auth/login-requests/req_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "PENDING"
    assert "access_token" not in data


def test_approve_login_request_generates_token(client, mock_db_cursor, mocker):
    """Responding with APPROVE generates and stores access token, updates FCM schema."""
    mocker.patch("app.api.routes.ensure_login_requests_columns")
    
    call_count = 0
    def mock_fetchone_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # Fetch request details
            return {
                "request_id": "req_123",
                "user_id": "parent_123",
                "user_type": "parent",
                "new_fcm_token": "new_fcm_token_123",
                "status": "PENDING",
                "expires_at": datetime.now() + timedelta(minutes=5)
            }
        elif call_count == 2:
            # Fetch parent phone
            return {"phone": 9876543210}
        elif call_count == 3:
            # Fetch old token
            return {"fcm_token": "old_fcm_token_abc"}
        return None

    mock_db_cursor.fetchone.side_effect = mock_fetchone_side_effect
    
    payload = {"action": "APPROVE"}
    response = client.post("/api/v1/auth/login-requests/req_123/respond", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Login request approved, tokens swapped"


def test_get_login_request_status_approved_claims_token(client, mock_db_cursor, mocker):
    """If approved, status returns token, then immediately updates request status to CLAIMED."""
    mocker.patch("app.api.routes.ensure_login_requests_columns")
    
    mock_db_cursor.fetchone.return_value = {
        "request_id": "req_123",
        "user_id": "parent_123",
        "user_type": "parent",
        "status": "APPROVED",
        "access_token": "generated_jwt_token_xyz",
        "expires_at": datetime.now() + timedelta(minutes=5)
    }
    
    response = client.get("/api/v1/auth/login-requests/req_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "APPROVED"
    assert data["access_token"] == "generated_jwt_token_xyz"


def test_get_login_request_status_expired(client, mock_db_cursor, mocker):
    """If request is expired, status returns EXPIRED."""
    mocker.patch("app.api.routes.ensure_login_requests_columns")
    
    mock_db_cursor.fetchone.return_value = {
        "request_id": "req_123",
        "user_id": "parent_123",
        "user_type": "parent",
        "status": "PENDING",
        "expires_at": datetime.now() - timedelta(minutes=5) # Expired 5 mins ago
    }
    
    response = client.get("/api/v1/auth/login-requests/req_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "EXPIRED"
