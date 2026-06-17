from tooling_demo import ServiceInfo, get_service_info


def test_get_service_info() -> None:
    assert get_service_info() == ServiceInfo(name="tooling-demo", version="0.1.0")
