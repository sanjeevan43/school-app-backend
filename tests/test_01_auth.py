import pytest
from fastapi import status

# With DEBUG=False:
#   - FirewallMiddleware hard-blocks /docs, /redoc, /openapi.json → 403 regardless of credentials.
#   - The Basic-Auth dependency on those routes never runs because the middleware intercepts first.

DOCS_PATHS = ["/docs", "/redoc", "/openapi.json"]

def test_get_swagger_documentation_unauthorized(client):
    """No credentials → firewall blocks → 403."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_swagger_documentation_with_auth(client, auth_headers):
    """Even with valid credentials, firewall still blocks in production (DEBUG=False) → 403."""
    response = client.get("/docs", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_redoc_documentation(client, auth_headers):
    response = client.get("/redoc", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_openapi_json(client, auth_headers):
    response = client.get("/openapi.json", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_root(client):
    """Root endpoint is accessible from allowed origins."""
    headers = {"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"}
    response = client.get("/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "School Transport Management API"
    assert "version" in data

def test_health_check(client, mock_db_cursor):
    headers = {"User-Agent": "Mozilla/5.0 Safari", "Origin": "https://transport.selvagam.com"}
    response = client.get("/health", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy", "database": "connected"}
