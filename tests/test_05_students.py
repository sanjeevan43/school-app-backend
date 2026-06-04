import pytest

HEADERS = {
    "User-Agent": "Mozilla/5.0 Safari",
    "Origin": "https://transport.selvagam.com"
}

def test_create_student(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "student_id": "test-student-id",
        "parent_id": None,
        "s_parent_id": None,
        "name": "Test Student",
        "gender": "MALE",
        "dob": "2010-01-01",
        "study_year": "2023-2024",
        "class_id": None,
        "pickup_route_id": None,
        "drop_route_id": None,
        "pickup_stop_id": None,
        "drop_stop_id": None,
        "emergency_contact": None,
        "student_photo_url": None,
        "student_status": "CURRENT",
        "transport_status": "ACTIVE",
        "is_transport_user": True,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.post("/api/v1/api/v1/students", json={
        "name": "Test Student",
        "gender": "MALE",
        "dob": "2010-01-01",
        "study_year": "2023-2024"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Test Student"

def test_get_all_students(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = [
        {
            "student_id": "test-student-id",
            "parent_id": None,
            "s_parent_id": None,
            "name": "Test Student",
            "gender": "MALE",
            "dob": "2010-01-01",
            "study_year": "2023-2024",
            "class_id": None,
            "pickup_route_id": None,
            "drop_route_id": None,
            "pickup_stop_id": None,
            "drop_stop_id": None,
            "emergency_contact": None,
            "student_photo_url": None,
            "student_status": "CURRENT",
            "transport_status": "ACTIVE",
            "is_transport_user": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]

    response = client.get("/api/v1/api/v1/students", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_student(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "student_id": "test-student-id",
        "parent_id": None,
        "s_parent_id": None,
        "name": "Test Student",
        "gender": "MALE",
        "dob": "2010-01-01",
        "study_year": "2023-2024",
        "class_id": None,
        "pickup_route_id": None,
        "drop_route_id": None,
        "pickup_stop_id": None,
        "drop_stop_id": None,
        "emergency_contact": None,
        "student_photo_url": None,
        "student_status": "CURRENT",
        "transport_status": "ACTIVE",
        "is_transport_user": True,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    response = client.get("/api/v1/api/v1/students/test-student-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["student_id"] == "test-student-id"

def test_update_student(client, mock_db_cursor):
    mock_db_cursor.fetchone.return_value = {
        "student_id": "test-student-id",
        "parent_id": None,
        "s_parent_id": None,
        "name": "Updated Student",
        "gender": "MALE",
        "dob": "2010-01-01",
        "study_year": "2023-2024",
        "class_id": None,
        "pickup_route_id": None,
        "drop_route_id": None,
        "pickup_stop_id": None,
        "drop_stop_id": None,
        "emergency_contact": None,
        "student_photo_url": None,
        "student_status": "CURRENT",
        "transport_status": "ACTIVE",
        "is_transport_user": True,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    mock_db_cursor.rowcount = 1

    response = client.put("/api/v1/api/v1/students/test-student-id", json={
        "name": "Updated Student"
    }, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Student"

def test_delete_student(client, mock_db_cursor):
    mock_db_cursor.rowcount = 1
    response = client.delete("/api/v1/api/v1/students/test-student-id", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted successfully"}
