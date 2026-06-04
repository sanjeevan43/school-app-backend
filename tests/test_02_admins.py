import pytest

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def test_create_admin(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "admin_id": "test-admin-id",
        "phone": 1234567890,
        "email": "admin@example.com",
        "name": "Test Admin",
        "status": "ACTIVE",
        "last_login_at": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.post("/api/v1/admins", json={
        "name": "Test Admin",
        "phone": 1234567890,
        "email": "admin@example.com"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Test Admin"

def test_get_all_admins(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {
            "admin_id": "test-admin-id",
            "phone": 1234567890,
            "email": "admin@example.com",
            "name": "Test Admin",
            "status": "ACTIVE",
            "last_login_at": None,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]

    response = client.get("/api/v1/admins", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_admin(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "admin_id": "test-admin-id",
        "phone": 1234567890,
        "email": "admin@example.com",
        "name": "Test Admin",
        "status": "ACTIVE",
        "last_login_at": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    response = client.get("/api/v1/admins/test-admin-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["admin_id"] == "test-admin-id"

def test_update_admin(client, mock_db_cursor):
    # The endpoint does a fetchone to get old_admin, then execute, then get_admin.
    # We will just set a generic fetchone that works for both old_admin and get_admin.
    mock_db_cursor.fetchone.return_value = {
        "admin_id": "test-admin-id",
        "phone": 1234567890,
        "email": "admin@example.com",
        "name": "Updated Admin",
        "status": "ACTIVE",
        "last_login_at": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.put("/api/v1/admins/test-admin-id", json={
        "name": "Updated Admin"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Admin"

def test_delete_admin(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    # delete_admin calls cascade_service.delete_cascades which might do something, but let's assume it works.
    response = client.delete("/api/v1/admins/test-admin-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"message": "Admin deleted successfully"}
