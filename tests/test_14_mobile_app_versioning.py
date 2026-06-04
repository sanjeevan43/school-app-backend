import pytest
from fastapi import status

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def test_check_app_version(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "app_type": "PARENT",
        "platform": "ANDROID",
        "minimum_supported_version": "1.0.0",
        "latest_version": "1.2.0",
        "update_message": "Update available"
    }
    payload = {
        "app_type": "PARENT",
        "platform": "ANDROID",
        "app_version": "1.1.0"
    }
    response = client.post("/api/v1/check-app-version", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["update_available"] is True

def test_get_all_app_versions(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {
            "id": "test_id",
            "app_type": "PARENT",
            "platform": "ANDROID",
            "minimum_supported_version": "1.0.0",
            "latest_version": "1.2.0",
            "force_update": False,
            "update_message": "Update available",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    ]
    response = client.get("/api/v1/app-versions", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_get_app_version(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "id": "test_id",
        "app_type": "PARENT",
        "platform": "ANDROID",
        "minimum_supported_version": "1.0.0",
        "latest_version": "1.2.0",
        "force_update": False,
        "update_message": "Update available",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    response = client.get("/api/v1/app-versions/test_id", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_create_app_version(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    mock_db_cursor.fetchone.return_value = {
        "id": "test_id",
        "app_type": "PARENT",
        "platform": "ANDROID",
        "minimum_supported_version": "1.0.0",
        "latest_version": "1.2.0",
        "force_update": False,
        "update_message": "Update available",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    payload = {
        "app_type": "PARENT",
        "platform": "ANDROID",
        "minimum_supported_version": "1.0.0",
        "latest_version": "1.2.0",
        "force_update": False,
        "update_message": "Update available"
    }
    response = client.post("/api/v1/app-versions", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_update_app_version(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    mock_db_cursor.fetchone.return_value = {
        "id": "test_id",
        "app_type": "PARENT",
        "platform": "ANDROID",
        "minimum_supported_version": "1.0.0",
        "latest_version": "1.3.0",
        "force_update": True,
        "update_message": "Update available",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    payload = {
        "latest_version": "1.3.0",
        "force_update": True
    }
    response = client.put("/api/v1/app-versions/test_id", json=payload, headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK

def test_delete_app_version(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/app-versions/test_id", headers=HEADERS)
    assert response.status_code == status.HTTP_200_OK
