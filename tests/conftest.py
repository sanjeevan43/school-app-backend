import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app

@pytest.fixture
def mock_db_cursor():
    """Mock database cursor with safe defaults that don't accidentally
    trigger 'has active records' guard checks in cascade_service.delete_cascades."""
    cursor_mock = MagicMock()
    # Default fetchone: return a basic valid record
    cursor_mock.fetchone.return_value = {"id": 1, "status": "ACTIVE"}
    # Default fetchall: return EMPTY so 'blocking dependency' checks pass cleanly.
    # Individual tests that need a non-empty list must set this themselves.
    cursor_mock.fetchall.return_value = []
    cursor_mock.rowcount = 1
    return cursor_mock

@pytest.fixture
def mock_db_connection(mock_db_cursor):
    """Mock database connection."""
    conn_mock = MagicMock()
    cursor_context = MagicMock()
    cursor_context.__enter__.return_value = mock_db_cursor
    conn_mock.cursor.return_value = cursor_context
    return conn_mock

@pytest.fixture(autouse=True)
def mock_database(mocker, mock_db_connection, mock_db_cursor):
    """Automatically mock database functions for all tests.

    FIX: Patch get_db in all modules that import it directly so that
    tests which call handlers using `with get_db() as conn:` (e.g. route-stops,
    bulk operations) don't hit the real database and get an Access Denied error.
    """
    get_db_mock = MagicMock()
    get_db_context = MagicMock()
    get_db_context.__enter__.return_value = mock_db_connection
    get_db_mock.return_value = get_db_context

    # Patch in the database module itself
    mocker.patch("app.core.database.get_db", get_db_mock)
    # Patch in routes.py (it imports get_db at module level)
    mocker.patch("app.api.routes.get_db", get_db_mock)
    # Patch in cascade_updates.py (used by delete handlers)
    mocker.patch("app.services.cascade_updates.get_db", get_db_mock)

    def mock_execute_query(query, params=None, fetch_one=False, fetch_all=False):
        if fetch_one:
            return mock_db_cursor.fetchone()
        elif fetch_all:
            return mock_db_cursor.fetchall()
        else:
            return mock_db_cursor.rowcount

    mocker.patch("app.core.database.execute_query", side_effect=mock_execute_query)
    # Also patch execute_query where it's used directly inside routes/services
    mocker.patch("app.api.routes.execute_query", side_effect=mock_execute_query)
    mocker.patch("app.services.cascade_updates.execute_query", side_effect=mock_execute_query)

    yield

@pytest.fixture(autouse=True)
def mock_firebase(mocker):
    """Mock Firebase push notifications."""
    mocker.patch("app.notification_api.service.messaging.send", return_value="mock-message-id")
    mocker.patch("app.notification_api.service.firebase_admin.initialize_app")
    mocker.patch("app.notification_api.service.firebase_admin.get_app")
    yield

@pytest.fixture(autouse=True)
def mock_debug_mode(mocker):
    """FIX: Force DEBUG=False for all tests so that:
       - The Firewall middleware enforces its /docs block (test_01_auth).
       - The docs Basic-Auth check runs instead of being bypassed.
    The get_settings() result is lru_cached so we patch the settings object directly."""
    from app.core.config import get_settings
    settings = get_settings()
    original = settings.DEBUG
    settings.DEBUG = False
    yield
    settings.DEBUG = original

@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def auth_headers():
    """Returns headers with correct Basic Auth credentials for Swagger access."""
    import base64
    from app.core.config import get_settings
    settings = get_settings()
    creds = f"{settings.DOCS_USERNAME}:{settings.DOCS_PASSWORD}".encode("utf-8")
    b64 = base64.b64encode(creds).decode("utf-8")
    return {
        "Authorization": f"Basic {b64}",
        "User-Agent": "Mozilla/5.0",
    }
