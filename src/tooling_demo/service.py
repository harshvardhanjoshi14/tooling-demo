"""Application metadata exposed by the library and API."""

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


def get_service_info() -> ServiceInfo:
    """Return the service metadata."""
    package = distribution("tooling-demo")
    return ServiceInfo(name=package.metadata["Name"], version=package.version)
