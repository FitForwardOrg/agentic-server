import pytest
from fastapi.testclient import TestClient

from src.api import WebServer
from src.api.health.handlers import HealthHandler
from src.config import Settings
from src.fine_tuner import factory


@pytest.fixture
def settings(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    s = Settings()
    return s


@pytest.fixture
def resume_tuner(settings):
    return factory(cfg=settings)


@pytest.fixture
def web_server(resume_tuner):
    server = WebServer(resume_tuner=resume_tuner)
    HealthHandler(server=server)
    return server


@pytest.fixture
def client(web_server):
    return TestClient(app=web_server.app)
