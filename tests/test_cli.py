from click.testing import CliRunner

from tooling_demo.cli import cli


def test_info_command() -> None:
    result = CliRunner().invoke(cli, ["info"])

    assert result.exit_code == 0
    assert '"name": "tooling-demo"' in result.output
