# tooling-demo

A small [FastAPI](https://fastapi.tiangolo.com/) service for exploring
[mise](https://mise.jdx.dev/), [uv](https://docs.astral.sh/uv/), and the rest of
a modern [Python](https://www.python.org/) toolchain. The repository stays
intentionally focused so each addition can be explained, tested, and eventually
carried into a project template.

## What it shows

- a pinned Python 3.12 `src/` package
- a reusable library with [FastAPI](https://fastapi.tiangolo.com/) and
  [Click](https://click.palletsprojects.com/) interfaces
- [mise](https://mise.jdx.dev/) for installing uv, activating the environment,
  and running project tasks
- [uv](https://docs.astral.sh/uv/) for runtime and development dependency
  management
- [pytest](https://docs.pytest.org/) and [Ruff](https://docs.astral.sh/ruff/) as
  development dependencies

## Install mise

This project requires mise 2026.6.10 or newer. The minimum is declared in
`mise.toml`, so older versions fail with an actionable upgrade message.

Follow the [official installation guide](https://mise.jdx.dev/getting-started/)
for all supported platforms and package managers. On Linux or macOS, the
standalone installer is:

```bash
curl https://mise.run | sh
```

Activate mise in your interactive shell so project tools and environment
variables load when you enter the repository. For zsh:

```bash
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc
exec zsh
```

For bash:

```bash
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
exec bash
```

If mise was installed somewhere other than `~/.local/bin`, replace that path
with the path to your mise executable. See the
[activation documentation](https://mise.jdx.dev/cli/activate.html) for other
shells and installation methods.

Verify the installation before setting up the project:

```bash
mise --version
mise doctor
```

## Quick start

```bash
mise trust
mise install
mise run setup
mise run validate-setup
mise run start-dev-server
```

`mise install` installs the tools declared in `mise.toml`. `setup` installs the
project dependencies, while `validate-setup` checks the environment and produces
a diagnostic report.

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

## Useful mise commands

| Command | Purpose |
| --- | --- |
| `mise doctor` | Diagnose the local mise installation. |
| `mise install` | Install tools declared in `mise.toml`. |
| `mise ls --current` | Show the tools and versions active for this project. |
| `mise tasks` | List the project's public tasks and their descriptions. |
| `mise tasks --hidden` | Include internal diagnostic tasks in the task list. |
| `mise config ls` | Show the configuration files mise loaded. |

## Development workflow

The repository exposes its development workflow as mise tasks. Run `mise tasks`
for the current command list and descriptions.

| Command | Purpose |
| --- | --- |
| `mise run setup` | Install the project dependencies. |
| `mise run install-dependencies` | Synchronize the uv project environment. |
| `mise run validate-setup` | Rerun diagnostics, linting, and tests. |
| `mise run start-dev-server` | Start the API with automatic reloads. |
| `mise run start-server` | Start the API without automatic reloads. |
| `mise run lint` | Check the codebase with Ruff. |
| `mise run format` | Format the codebase with Ruff. |
| `mise run run-tests` | Run the pytest test suite. |

These tasks are intentionally explicit. Developers can run the smallest useful
check while working, and `validate-setup` provides the complete safety net. A
later iteration will use [prek](https://prek.j178.dev/) to automate the relevant
checks before a commit without removing the underlying commands.

## Current focus

The first article will introduce the setup problem and dive into `mise`.

Later articles will extend this repo with:

- [prek](https://prek.j178.dev/)-based commit checks
- CI that mirrors the local command surface
