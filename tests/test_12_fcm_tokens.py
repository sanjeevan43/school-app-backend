import pytest
from fastapi import status
from unittest.mock import MagicMock

HEADERS = {"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"}

def test_create_fcm_token(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "fcm_id": "test_fcm_123",
        "fcm_token": "test_token_123",
        "student_id": "test_student_123",
        "parent_id": None
    }
    
    payload = {
        "fcm_token": "test_token_123",
        "student_id": "test_student_123"
    }
    
    response = client.post("/api/v1/fcm-tokens", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["fcm_id"] == "test_fcm_123"

def test_get_all_fcm_tokens(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {"fcm_id": "test_fcm_123", "fcm_token": "test_token_123"}
    ]
    
    response = client.get("/api/v1/fcm-tokens", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert "fcm_tokens" in response.json()

def test_get_fcm_token(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "fcm_id": "test_fcm_123",
        "fcm_token": "test_token_123",
        "student_id": "test_student_123",
        "parent_id": None
    }
    
    response = client.get("/api/v1/fcm-tokens/test_fcm_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["fcm_id"] == "test_fcm_123"

def test_update_fcm_token(client, mock_db_cursor, mocker):
    mock_db_cursor.fetchone.return_value = {
        "fcm_id": "test_fcm_123",
        "fcm_token": "new_test_token",
        "student_id": "test_student_123",
        "parent_id": None
    }
    mock_db_cursor.rowcount = 1
    
    mocker.patch("app.api.routes.cascade_service.update_fcm_token_cascades")
    
    payload = {
        "fcm_token": "new_test_token"
    }
    
    response = client.put("/api/v1/fcm-tokens/test_fcm_123", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_delete_fcm_token(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    
    response = client.delete("/api/v1/fcm-tokens/test_fcm_123", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "FCM token deleted successfully"
