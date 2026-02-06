from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from src.api.errors import NotFoundError


def test_not_found_error_handler(web_server):
    """Test that NotFoundError is correctly handled and returns a 404 JSON response."""

    @web_server.app.get("/trigger-404")
    async def trigger_404():
        raise NotFoundError("Test resource not found")

    client = TestClient(web_server.app)
    response = client.get("/trigger-404")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["success"] is False
    assert data["error"]["message"] == "Test resource not found"
    assert data["error"]["code"] == "NOT_FOUND"


def test_generic_exception_handler(web_server, resume_tuner):
    """Test that generic exceptions are correctly handled and return a 500 JSON response."""
    with patch.object(resume_tuner, "is_ready", side_effect=Exception("Test exception")):
        client = TestClient(web_server.app, raise_server_exceptions=False)
        response = client.get("/api/health/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert data["success"] is False
        assert data["error"]["message"] == "An unexpected error occurred"
        assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
