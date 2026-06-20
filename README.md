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
- [mise](https://mise.jdx.dev/) for installing uv and
  [prek](https://prek.j178.dev/), activating the environment, and running
  project tasks
- [uv](https://docs.astral.sh/uv/) for runtime and development dependency
  management
- [pytest](https://docs.pytest.org/), [Ruff](https://docs.astral.sh/ruff/), and
  [ty](https://docs.astral.sh/ty/) as development dependencies
- a familiar [pre-commit](https://pre-commit.com/) configuration executed by
  prek for formatting, linting, repository hygiene, and commit-message checks

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
project dependencies and Git hooks, while `validate-setup` checks the
environment and produces a diagnostic report.

The API is available at `http://127.0.0.1:8000`, with runtime diagnostics at
`http://127.0.0.1:8000/runtime` and interactive documentation at
`http://127.0.0.1:8000/docs`.

Run the installed package's CLI directly through uv when needed:

```bash
uv run tooling-demo info
uv run tooling-demo runtime
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
| `mise run setup` | Install dependencies and prepare the Git hooks. |
| `mise run install-dependencies` | Synchronize the uv project environment. |
| `mise run install-git-hooks` | Install and prepare the prek-managed Git hooks. |
| `mise run validate-setup` | Rerun diagnostics, pre-commit checks, and tests. |
| `mise run start-dev-server` | Start the API with automatic reloads. |
| `mise run start-server` | Start the API without automatic reloads. |
| `mise run pre-commit` | Run every pre-commit check against the repository. |
| `mise run run-tests` | Run the pytest test suite. |

The pre-commit task is the repository's formatting and static-analysis entry
point, while `validate-setup` adds diagnostics and tests as the complete safety
net. `mise run pre-commit` intentionally fails on `main`; `validate-setup`
skips only that branch guard so diagnostics can run from any branch. Run an
individual hook through prek when narrower feedback is useful:

```bash
prek run ruff-check --all-files
prek run ruff-format --all-files
prek run ty-check --all-files
prek run uv-lock --all-files
```

The configured `pre-commit` and `commit-msg` Git hooks run the relevant checks
automatically during normal development. See the
[contribution guide](CONTRIBUTING.md) for the human-facing Python style and
commit conventions behind those checks.

## Current focus

The first article introduces the setup problem and dives into `mise`. The second
adds prek-based formatting, linting, repository hygiene, and commit-message
validation.

Later articles will extend this repo with:

- CI that mirrors the local command surface
- changelog generation from Conventional Commits
