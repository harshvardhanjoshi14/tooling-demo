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

- Target Python 3.12.
- Keep importable code under `src/tooling_demo/` and tests under `tests/`.
- Add type annotations to functions and verify them with
  [ty](https://docs.astral.sh/ty/).
- Write Google-style docstrings for public modules, classes, and functions.
- Add `Args`, `Returns`, and `Raises` sections when the public contract needs
  them; do not repeat information already clear from the signature.
- Use [Ruff](https://docs.astral.sh/ruff/) for formatting, import ordering, and
  linting.

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
- Separate Given, When, and Then phases with whitespace. Add phase comments only
  when the boundaries are not obvious.
- Give tests behavior-focused names such as `test_returns_service_metadata`.
- Use test classes only when they provide useful grouping or shared context.
- Keep tests typed, but do not require docstrings that merely repeat test names.
- Add regression coverage for bug fixes and tests for newly introduced behavior.

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

Work on a branch rather than committing directly to `main`. Keep each commit
focused on one coherent change.

## Before opening a pull request

Run the complete local safety net:

```bash
mise run validate-setup
```

It prints environment diagnostics, runs every content-oriented pre-commit check,
type-checks the project, and executes the test suite. Branch protection is
skipped only for this diagnostic aggregate; normal commits still enforce it.
