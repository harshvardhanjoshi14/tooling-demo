"""HTTP interface for the tooling demo service."""

from fastapi import FastAPI

from tooling_demo.service import (
    HealthStatus,
    RuntimeInfo,
    ServiceInfo,
    get_runtime_info,
    get_service_info,
)

service = get_service_info()

app = FastAPI(
    title="Tooling Demo",
    description="A small API for demonstrating a modern Python toolchain.",
    version=service.version,
)


@app.get("/", response_model=ServiceInfo)
def service_info() -> ServiceInfo:
    """Return identifying information about the service."""
    return get_service_info()


@app.get("/health", response_model=HealthStatus)
def health() -> HealthStatus:
    """Report whether the service is ready to receive requests."""
    return HealthStatus()


@app.get("/runtime", response_model=RuntimeInfo)
def runtime_info() -> RuntimeInfo:
    """Return information about the Python runtime hosting the service."""
    return get_runtime_info()
