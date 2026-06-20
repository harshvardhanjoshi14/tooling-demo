import platform

from fastapi.testclient import TestClient

from tooling_demo.api import app

client = TestClient(app)


def test_service_info() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"name": "tooling-demo", "version": "0.1.0"}


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_runtime_info() -> None:
    response = client.get("/runtime")

    assert response.status_code == 200
    assert response.json() == {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }
