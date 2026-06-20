"""Application metadata exposed by the library and API."""

import platform
from importlib.metadata import distribution
from typing import Literal

from pydantic import BaseModel


class ServiceInfo(BaseModel):
    """Public information about this service."""

    name: str
    version: str


class HealthStatus(BaseModel):
    """Health information returned by the API."""

    status: Literal["ok"] = "ok"


class RuntimeInfo(BaseModel):
    """Information about the Python runtime hosting the service."""

    python_implementation: str
    python_version: str


def get_service_info() -> ServiceInfo:
    """Return the service metadata."""
    package = distribution("tooling-demo")
    return ServiceInfo(name=package.metadata["Name"], version=package.version)


def get_runtime_info() -> RuntimeInfo:
    """Return information about the active Python runtime.

    Returns:
        RuntimeInfo: The Python implementation and version running the service.
    """
    return RuntimeInfo(
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
    )
