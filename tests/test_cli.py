import json
import platform

from click.testing import CliRunner

from tooling_demo.cli import cli


def test_info_command() -> None:
    result = CliRunner().invoke(cli, ["info"])

    assert result.exit_code == 0
    assert '"name": "tooling-demo"' in result.output


def test_runtime_command() -> None:
    result = CliRunner().invoke(cli, ["runtime"])

    assert result.exit_code == 0
    assert json.loads(result.output) == {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }
