# Contributing

This repository keeps its development contract small, explicit, and executable.
The goal is to make reviews about behavior and design rather than formatting,
imports, or machine-specific setup.

Start by installing [mise](https://mise.jdx.dev/), then prepare the project and
its Git hooks:

```bash
mise trust
mise install
mise run setup
mise run validate-setup
```

## Python style

- Target Python 3.12 and use modern Python syntax where it improves clarity.
- Keep importable code under `src/tooling_demo/` and tests under `tests/`.
- Prefer small functions with explicit inputs, focused responsibilities, and
  meaningful return values.
- Add type annotations to functions. Avoid `Any` and suppression comments unless
  the boundary genuinely cannot be expressed more precisely.
- Write Google-style docstrings for public modules, classes, and functions.
- Document `Args`, `Returns`, and `Raises` when they add information beyond the
  signature. Explain the contract rather than restating the implementation.
- Let [Ruff](https://docs.astral.sh/ruff/) own formatting, import ordering, and
  linting rather than applying personal formatting preferences.
- Use [ty](https://docs.astral.sh/ty/) to verify that annotations agree with how
  values move through the program.

The authoritative Ruff and ty policies live in `pyproject.toml`. Run the
complete set of formatters and static checks with:

```bash
mise run pre-commit
```

Run an individual hook when you need narrower feedback:

```bash
prek run ruff-check --all-files
prek run ruff-format --all-files
prek run ty-check --all-files
```

Some hooks modify files. Review those changes, stage them, and rerun the checks
instead of bypassing the hook.

## Tests

- Test observable behavior rather than implementation details.
- Structure each test as Given, When, Then, using whitespace to keep those phases
  visible. Add phase comments only when the boundaries are not obvious.
- Give tests behavior-focused names such as `test_returns_service_metadata`.
- Group tests in a class only when the class communicates a useful shared
  behavior or context.
- Keep tests typed, but do not require docstrings that merely repeat test names.
- Add a regression test with every bug fix and cover both success and failure
  paths when introducing behavior.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```text
<type>[optional scope]: <description>
```

For example:

```text
feat(api): add a health endpoint
fix(cli): reject invalid port numbers
docs: explain the local quality checks
```

[Commitizen](https://commitizen-tools.github.io/commitizen/) validates this
format through the `commit-msg` Git hook installed by `mise run setup`.

Work on a focused branch rather than committing directly to `main`. Keep commits
small enough that each one describes a coherent change and can be reviewed on
its own.

## Before opening a pull request

Run the complete local safety net:

```bash
mise run validate-setup
```

It prints environment diagnostics, runs every content-oriented pre-commit check,
type-checks the project, and executes the test suite. Branch protection is
skipped only for this diagnostic aggregate; normal commits still enforce it.
