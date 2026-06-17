# A better first day in a Python repository with mise

You have just joined a team. You clone the backend repository, open the README,
and want to make a useful change before the end of the day.

Instead, the first hour becomes a scavenger hunt:

- Which Python version does this project use?
- How should the virtual environment be created?
- Which package manager should I use?
- What is the command to run the tests?
- Is the command in the README still current?
- Why does the application work for everyone except me?

None of these questions is difficult. That is almost what makes the situation
annoying. Every answer is usually written down somewhere, but a developer still
has to find it, interpret it, and reproduce it correctly.

I wanted a repository with a smaller first-day contract:

```bash
mise run setup
```

That command prepares the project, validates the result, and produces useful
diagnostics when something does not work.

This article builds that workflow for a small Python service. Python is the
example, but most of the mise setup applies just as well to a Go service, a
Terraform repository, or a project containing several toolchains.

The complete example lives in the `tooling-demo` repository. It is a small
FastAPI service with a Click command-line interface, a `src/` package layout,
and tests. The application is intentionally modest. The development experience
is what we are examining.

## What mise is doing here

[mise](https://mise.jdx.dev/) describes itself as a tool for development tools,
environment variables, and tasks. That combination is the interesting part.

A version manager can put the correct executable on `PATH`. A task runner can
remember commands. A shell configuration can activate an environment. mise can
connect those jobs through one project configuration file.

For this repository, mise has three responsibilities:

1. Install and select the project's pinned uv version.
2. Activate the project's `.venv` when it exists.
3. Provide a discoverable set of development commands.

uv owns the Python-specific work. It reads `.python-version`, installs Python
when the requested version is unavailable, creates `.venv`, and synchronizes
the project dependencies. The [uv Python documentation](https://docs.astral.sh/uv/concepts/python-versions/)
describes both its Python discovery rules and managed Python downloads.

That division is intentional:

```text
mise -> installs uv and exposes project tasks
uv   -> installs Python and manages the Python environment
```

There is no reason for two tools to manage the same Python installation.

## Pin the first tool

The repository starts its `mise.toml` with one tool:

```toml
[tools]
uv = "0.11.21"
```

This is already useful. A new developer does not need to install uv separately,
and two developers will not accidentally use different uv releases because one
of them installed it six months later.

mise supports many tools and several installation backends, all behind the
same `[tools]` configuration. Its [development tools documentation](https://mise.jdx.dev/dev-tools/)
goes deeper into resolution, installation, activation, and the available
backends.

For now, one pinned tool is enough. I would rather add tools when the repository
has a reason to use them than turn `mise.toml` into a collection of things that
look useful.

## Let uv own Python

The Python version is declared separately in `.python-version`:

```text
3.12.13
```

The project also states its supported Python range in `pyproject.toml`:

```toml
[project]
requires-python = ">=3.12"
```

These declarations answer related but different questions. `requires-python`
is package metadata: it describes which Python versions the project supports.
`.python-version` selects the concrete interpreter used for development in this
repository.

When `uv sync` runs, uv respects `.python-version`. If that interpreter is not
available, uv can download it automatically. It then creates `.venv`, resolves
the dependencies, and installs the project as an editable package. The behavior
of syncing and editable installs is documented in [uv's project sync guide](https://docs.astral.sh/uv/concepts/projects/sync/).

This gives us a small bootstrap chain:

```text
mise -> uv 0.11.21 -> Python 3.12.13 -> .venv -> project dependencies
```

Only mise needs to be installed before entering the repository.

## Make the environment disappear into the workflow

Creating a virtual environment is only half the job. Developers also need their
shell and tools to use it consistently.

The next part of `mise.toml` handles that:

```toml
[settings]
python.uv_venv_auto = "create|source"
task.output = "keep-order"

[env]
_.python.venv = { path = ".venv" }
```

The `uv_venv_auto` setting connects mise's Python environment handling to uv.
The value allows the environment to be created when necessary and sourced when
it is available. The `[env]` directive identifies `.venv` as the project virtual
environment. The task output setting becomes useful later, when several
diagnostic tasks run concurrently but their output still needs to be readable.

After mise is activated in the shell, entering the repository is enough for the
project environment to become active. There is no platform-specific activation
command to remember and no opportunity for the README to recommend a stale
path.

Because project configuration can affect the shell and run commands, mise has a
trust mechanism. On the first visit to a cloned repository, run:

```bash
mise trust
```

Trust is explicit and local. mise will not blindly evaluate a newly cloned
configuration. The exact behavior is covered by the [`mise trust` reference](https://mise.jdx.dev/cli/trust.html).

## Turn the README into executable commands

The smallest useful operation is deliberately boring:

```toml
[tasks.install-dependencies]
description = "Install the project dependencies"
run = "uv sync"
```

It is idempotent: running it again brings the environment to the same declared
state. The public setup command composes that operation with validation:

```toml
[tasks.setup]
description = "Install and validate the development environment"
run = [
    { task = "install-dependencies" },
    { task = "validate-setup" },
]
```

Entries in a `run` array execute sequentially. Dependencies must be installed
before validation begins, so the order is part of the workflow rather than a
comment in the README.

The onboarding instruction remains small:

```bash
mise run setup
```

That command installs the pinned uv version when needed. uv then installs the
requested Python version, creates `.venv`, and installs the project. Finally,
the validation task checks the resulting environment.

The important property is not that `uv sync` is hard to type. It is that the
repository owns the command. If the setup grows later, the onboarding interface
does not need to change.

The rest of the local workflow uses the same pattern:

```toml
[tasks.start-dev-server]
description = "Run the API with automatic reloads"
run = "uv run tooling-demo serve --reload"

[tasks.run-tests]
description = "Run the test suite"
run = "uv run pytest"

[tasks.lint]
description = "Check the codebase with Ruff"
run = "uv run ruff check ."

[tasks.format]
description = "Format the codebase with Ruff"
run = "uv run ruff format ."
```

The descriptions are not decoration. mise includes them when listing tasks, so
the configuration becomes a small, executable help system:

```bash
mise tasks
```

```text
format            Format the codebase with Ruff
install-dependencies  Install the project dependencies
lint              Check the codebase with Ruff
run-tests         Run the test suite
setup             Install and validate the development environment
start-dev-server  Run the API with automatic reloads
start-server      Run the API
validate-setup    Print diagnostics and validate the development setup
```

mise tasks can be simple commands or structured workflows with dependencies,
arguments, environment variables, and platform-specific variants. The complete
surface is in the [task configuration reference](https://mise.jdx.dev/tasks/task-configuration.html).

## Keep application commands in the application

There is a boundary worth preserving here.

The FastAPI service is launched through an installed Click command:

```bash
uv run tooling-demo serve --reload
```

mise provides the convenient repository command:

```bash
mise run start-dev-server
```

These are not competing interfaces. The package owns how the application runs;
mise owns the day-to-day repository workflow. Someone who installs the package
still gets a useful CLI, while someone working in the repository gets one
consistent command alongside setup, tests, and linting.

## Validate setup, do not just hope

A setup command that fails with a useful error is good. A setup command that
appears successful while leaving a broken environment is much harder to debug.

The repository also exposes validation independently:

```bash
mise run validate-setup
```

Validation is assembled from small diagnostic tasks:

```toml
[tasks.validate-setup]
description = "Print diagnostics and validate the development setup"
depends = [
    "diagnose-mise",
    "diagnose-uv",
    "diagnose-python",
    "diagnose-environment",
    "diagnose-application",
    "lint",
    "run-tests",
]
run = 'echo "Setup validation passed."'
```

Unlike the ordered setup steps, these dependencies do not need to wait for one
another. mise builds a task graph and runs independent dependencies in parallel.
If any dependency fails, the final success message does not run.

The earlier `task.output = "keep-order"` setting buffers the parallel branches
and prints each result as one coherent block. We keep the speed of concurrent
checks without turning the diagnostic report into interleaved terminal soup.

Each diagnostic is still an ordinary task. For example:

```toml
[tasks.diagnose-uv]
hide = true
run = '''
echo "== uv =="
uv --version
'''

[tasks.diagnose-environment]
hide = true
run = '''
echo "== project environment =="
uv pip check
uv pip list
'''
```

The helper tasks are hidden from the default task listing. They remain directly
callable when debugging, but they do not overwhelm the everyday command surface.

Together, the diagnostics print:

- the mise version and active tools;
- the Python version and executable path;
- the uv version;
- the Python version inside the project environment;
- installed package versions;
- application metadata;
- lint and test results.

It also runs `uv pip check`, which verifies that the installed packages have
compatible dependencies.

The output serves two purposes. It gives the developer immediate confidence
that the repository works, and it produces a useful diagnostic bundle to paste
into an issue when it does not.

There is no custom onboarding framework to maintain, and adding another check
later means adding one small task and one edge to the graph.

## The complete first run

With mise installed and activated in your shell, the whole path is:

```bash
git clone <repository-url>
cd tooling-demo

mise trust
mise run setup
mise run start-dev-server
```

Because `setup` includes validation, that is the complete onboarding path.
`mise run validate-setup` remains useful when you only want to rerun diagnostics.

The API is then available at `http://127.0.0.1:8000`, with FastAPI's interactive
documentation at `http://127.0.0.1:8000/docs`.

From there, the common development commands are easy to discover and consistent
across machines:

```bash
mise run run-tests
mise run lint
mise run format
```

## What this does not solve yet

This repository is not finished, and that is useful.

`uv run` and `uv sync` can update `uv.lock` when project metadata changes. We do
not yet verify that a dependency edit includes the corresponding lockfile
change. We also do not run checks before a commit, and there is no CI workflow
proving that the local commands behave the same way on a clean machine.

Those are the next problems to solve, not details to hide in this article.

The next steps for the repository are:

1. Examine uv's project and dependency workflow in more depth.
2. Add `prek` so fast checks and lockfile validation happen before a commit.
3. Add CI that calls the same repository-owned commands used locally.
4. Turn the accumulated structure into a reusable project template.

For this first pass, the result is intentionally small: one pinned bootstrap
tool, one Python version declaration, an automatically managed environment, and
a command surface that a new developer can discover without archaeology.

That is enough to turn the first hour in a repository back into engineering.
