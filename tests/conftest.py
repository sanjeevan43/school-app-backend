import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app

@pytest.fixture
def mock_db_cursor():
    """Mock database cursor."""
    cursor_mock = MagicMock()
    # By default, fetchone/fetchall return empty or dummy data
    cursor_mock.fetchone.return_value = {"id": 1, "status": "ACTIVE"}
    cursor_mock.fetchall.return_value = [{"id": 1, "status": "ACTIVE"}]
    cursor_mock.rowcount = 1
    return cursor_mock

@pytest.fixture
def mock_db_connection(mock_db_cursor):
    """Mock database connection."""
    conn_mock = MagicMock()
    # Mock the context manager for connection.cursor()
    cursor_context = MagicMock()
    cursor_context.__enter__.return_value = mock_db_cursor
    conn_mock.cursor.return_value = cursor_context
    return conn_mock

@pytest.fixture(autouse=True)
def mock_database(mocker, mock_db_connection, mock_db_cursor):
    """Automatically mock database functions for all tests."""
    
    # Mock get_db context manager
    get_db_mock = MagicMock()
    get_db_context = MagicMock()
    get_db_context.__enter__.return_value = mock_db_connection
    get_db_mock.return_value = get_db_context
    
    mocker.patch("app.core.database.get_db", get_db_mock)
    mocker.patch("app.api.routes.get_db", get_db_mock)
    mocker.patch("app.services.cascade_updates.get_db", get_db_mock)
    
    # Mock execute_query
    def mock_execute_query(query, params=None, fetch_one=False, fetch_all=False):
        if fetch_one:
            return mock_db_cursor.fetchone()
        elif fetch_all:
            return mock_db_cursor.fetchall()
        else:
            return mock_db_cursor.rowcount

    mocker.patch("app.core.database.execute_query", side_effect=mock_execute_query)
    mocker.patch("app.api.routes.execute_query", side_effect=mock_execute_query)
    mocker.patch("app.services.cascade_updates.execute_query", side_effect=mock_execute_query)
    
    # Force DEBUG=False during tests
    from app.core.config import get_settings
    settings = get_settings()
    old_debug = settings.DEBUG
    settings.DEBUG = False
    
    yield
    
    settings.DEBUG = old_debug
    
@pytest.fixture(autouse=True)
def mock_firebase(mocker):
    """Mock Firebase push notifications."""
    mocker.patch("app.notification_api.service.messaging.send", return_value="mock-message-id")
    mocker.patch("app.notification_api.service.firebase_admin.initialize_app")
    mocker.patch("app.notification_api.service.firebase_admin.get_app")
    yield

@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """Returns headers with basic auth for Swagger access."""
    # Based on the main.py auth implementation (assuming admin/admin for basic tests)
    import base64
    auth_str = "admin:admin".encode("utf-8")
    b64_auth_str = base64.b64encode(auth_str).decode("utf-8")
    return {"Authorization": f"Basic {b64_auth_str}", "User-Agent": "Mozilla/5.0"}
