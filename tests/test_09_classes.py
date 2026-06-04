import pytest
from fastapi.testclient import TestClient

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def mock_class_data():
    return {
        "class_id": "class123",
        "class_name": "Class 1",
        "section": "A",
        "status": "ACTIVE",
        "number_of_students": 10,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

def test_create_class(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_class_data()
    payload = {
        "class_name": "Class 1",
        "section": "A"
    }
    response = client.post("/api/v1/classes", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["class_id"] == "class123"
    assert data["class_name"] == "Class 1"

def test_get_classes(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [mock_class_data()]
    response = client.get("/api/v1/classes", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["class_id"] == "class123"

def test_get_class(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_class_data()
    response = client.get("/api/v1/classes/class123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["class_id"] == "class123"

def test_update_class(client: TestClient, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = mock_class_data()
    payload = {
        "section": "B"
    }
    response = client.put("/api/v1/classes/class123", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["class_id"] == "class123"

def test_delete_class(client: TestClient, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/classes/class123", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "deleted" in data.get("message", "").lower()
