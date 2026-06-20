import pytest

from tooling_demo import RuntimeInfo, ServiceInfo, get_runtime_info, get_service_info


def test_get_service_info() -> None:
    assert get_service_info() == ServiceInfo(name="tooling-demo", version="0.1.0")


def test_get_runtime_info(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("platform.python_implementation", lambda: "CPython")
    monkeypatch.setattr("platform.python_version", lambda: "3.12.0")

    runtime = get_runtime_info()

    assert runtime == RuntimeInfo(
        python_implementation="CPython",
        python_version="3.12.0",
    )
