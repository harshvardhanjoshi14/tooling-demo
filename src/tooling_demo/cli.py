"""Command-line interface for the tooling demo service."""

import json

import click
import uvicorn

from tooling_demo.service import get_runtime_info, get_service_info


@click.group()
def cli() -> None:
    """Run and inspect the tooling demo service."""


@cli.command()
def info() -> None:
    """Print information about the service."""
    click.echo(json.dumps(get_service_info().model_dump(), indent=2))


@cli.command()
def runtime() -> None:
    """Print information about the active Python runtime."""
    click.echo(json.dumps(get_runtime_info().model_dump(), indent=2))


@cli.command()
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=8000, show_default=True, type=click.IntRange(1, 65535))
@click.option("--reload", is_flag=True, help="Reload when application files change.")
def serve(host: str, port: int, reload: bool) -> None:
    """Start the FastAPI service."""
    uvicorn.run("tooling_demo.api:app", host=host, port=port, reload=reload)
