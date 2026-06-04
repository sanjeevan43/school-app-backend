import pytest

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def test_create_parent(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "parent_id": "test-parent-id",
        "phone": 9876543210,
        "email": "parent@example.com",
        "name": "Test Parent",
        "parent_role": "FATHER",
        "door_no": "123",
        "street": "Main St",
        "city": "Test City",
        "district": "Test District",
        "pincode": "123456",
        "parents_active_status": "ACTIVE",
        "last_login_at": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.post("/api/v1/api/v1/parents", json={
        "name": "Test Parent",
        "phone": 9876543210,
        "email": "parent@example.com",
        "parent_role": "FATHER",
        "door_no": "123",
        "street": "Main St",
        "city": "Test City",
        "district": "Test District",
        "pincode": "123456"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Test Parent"

def test_get_all_parents(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {
            "parent_id": "test-parent-id",
            "phone": 9876543210,
            "email": "parent@example.com",
            "name": "Test Parent",
            "parent_role": "FATHER",
            "door_no": "123",
            "street": "Main St",
            "city": "Test City",
            "district": "Test District",
            "pincode": "123456",
            "parents_active_status": "ACTIVE",
            "last_login_at": None,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]

    response = client.get("/api/v1/api/v1/parents", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_parent(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "parent_id": "test-parent-id",
        "phone": 9876543210,
        "email": "parent@example.com",
        "name": "Test Parent",
        "parent_role": "FATHER",
        "door_no": "123",
        "street": "Main St",
        "city": "Test City",
        "district": "Test District",
        "pincode": "123456",
        "parents_active_status": "ACTIVE",
        "last_login_at": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    response = client.get("/api/v1/api/v1/parents/test-parent-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["parent_id"] == "test-parent-id"

def test_update_parent(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "parent_id": "test-parent-id",
        "phone": 9876543210,
        "email": "parent@example.com",
        "name": "Updated Parent",
        "parent_role": "FATHER",
        "door_no": "123",
        "street": "Main St",
        "city": "Test City",
        "district": "Test District",
        "pincode": "123456",
        "parents_active_status": "ACTIVE",
        "last_login_at": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.put("/api/v1/api/v1/parents/test-parent-id", json={
        "name": "Updated Parent"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Parent"

def test_delete_parent(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/api/v1/parents/test-parent-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"message": "Parent deleted successfully"}
