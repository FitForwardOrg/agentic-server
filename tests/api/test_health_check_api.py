from unittest.mock import patch


class TestHealthCheckEndpoint:
    """
    GET /api/health/alive  - service liveness probe
    GET /api/health/ready - service readiness probe
    """

    def test_when_svc_is_started_then_is_alive_returns_200(self, client):
        """liveness probe should return 200 OK"""
        response = client.get("/api/health/alive")
        assert response.status_code == 200
        assert response.json() == {"status": "alive"}

    def test_when_all_deps_are_ready_then_is_ready_returns_200(self, client, resume_tuner):
        """readiness probe should return 200 OK when all dependencies are ready"""
        with patch.object(resume_tuner, "is_ready", return_value=True):
            response = client.get("/api/health/ready")
            assert response.status_code == 200
            assert response.json() == {"status": "ready"}

    def test_when_deps_are_not_ready_then_is_ready_returns_503(self, client, resume_tuner):
        """readiness probe should return 503 Service Unavailable when dependencies are not ready"""
        with patch.object(resume_tuner, "is_ready", return_value=False):
            response = client.get("/api/health/ready")
            assert response.status_code == 503
            assert response.json() == {"status": "not ready"}
