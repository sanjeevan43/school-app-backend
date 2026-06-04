import pytest
from fastapi import status

def test_get_swagger_documentation(client, auth_headers):
    # Firewall blocks docs regardless of auth
    response = client.get("/docs", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_swagger_documentation_unauthorized(client):
    response = client.get("/docs")
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_redoc_documentation(client, auth_headers):
    response = client.get("/redoc", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_openapi_json(client, auth_headers):
    response = client.get("/openapi.json", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_root(client):
    # Assuming direct browser access or unauthorized origin returns 403 based on test_firewall
    # With a custom origin it should be 200
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
