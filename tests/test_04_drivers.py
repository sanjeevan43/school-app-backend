import pytest

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def test_create_driver(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "driver_id": "test-driver-id",
        "name": "Test Driver",
        "phone": 1234567890,
        "email": "driver@example.com",
        "licence_number": "LIC123",
        "licence_expiry": "2025-12-31",
        "photo_url": "http://example.com/photo.jpg",
        "fcm_token": None,
        "status": "ACTIVE",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.post("/api/v1/api/v1/drivers", json={
        "name": "Test Driver",
        "phone": 1234567890,
        "email": "driver@example.com",
        "licence_number": "LIC123",
        "licence_expiry": "2025-12-31"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Test Driver"

def test_get_all_drivers(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {
            "driver_id": "test-driver-id",
            "name": "Test Driver",
            "phone": 1234567890,
            "email": "driver@example.com",
            "licence_number": "LIC123",
            "licence_expiry": "2025-12-31",
            "photo_url": "http://example.com/photo.jpg",
            "fcm_token": None,
            "status": "ACTIVE",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]

    response = client.get("/api/v1/api/v1/drivers", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_driver(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "driver_id": "test-driver-id",
        "name": "Test Driver",
        "phone": 1234567890,
        "email": "driver@example.com",
        "licence_number": "LIC123",
        "licence_expiry": "2025-12-31",
        "photo_url": "http://example.com/photo.jpg",
        "fcm_token": None,
        "status": "ACTIVE",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    response = client.get("/api/v1/api/v1/drivers/test-driver-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["driver_id"] == "test-driver-id"

def test_update_driver(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "driver_id": "test-driver-id",
        "name": "Updated Driver",
        "phone": 1234567890,
        "email": "driver@example.com",
        "licence_number": "LIC123",
        "licence_expiry": "2025-12-31",
        "photo_url": "http://example.com/photo.jpg",
        "fcm_token": None,
        "status": "ACTIVE",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.put("/api/v1/api/v1/drivers/test-driver-id", json={
        "name": "Updated Driver"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Driver"

def test_delete_driver(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/api/v1/drivers/test-driver-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"message": "Driver deleted successfully"}
