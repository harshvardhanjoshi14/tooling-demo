# tooling-demo

A small FastAPI service for exploring `mise`, `uv`, and the rest of a modern
Python toolchain. The repository stays intentionally focused so each addition
can be explained, tested, and eventually carried into a project template.

## What it shows

- a pinned Python 3.12 `src/` package
- a reusable library with FastAPI and Click interfaces
- `mise` for installing uv, activating the environment, and running project tasks
- `uv` for runtime and development dependency management
- pytest and Ruff as development dependencies

## Quick start

```bash
mise trust
mise run setup
mise run start-dev-server
```

`setup` installs the dependencies and validates the environment. Run
`mise run validate-setup` separately whenever you need a fresh diagnostic report.

The API is available at `http://127.0.0.1:8000`, with interactive documentation
at `http://127.0.0.1:8000/docs`.

Run the installed package's CLI directly through uv when needed:

```bash
uv run tooling-demo info
uv run tooling-demo serve --help
```

The package CLI owns how the application runs. The mise tasks are convenient,
repository-level aliases, so `mise run start-dev-server` and `uv run
tooling-demo serve --reload` start the same application.

If mise prompts for trust, that is expected because the repository configures
the project virtual environment in `mise.toml`.

## Current focus

The first article will introduce the setup problem and dive into `mise`.

Later articles will extend this repo with:

- `prek`-based commit checks
- CI that mirrors the local command surface
