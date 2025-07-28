import pytest
from typer.testing import CliRunner

from gk6.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])

    if result.exit_code != 0:
        pytest.fail(f"Expected exit code 0, got {result.exit_code}")

    if "Usage:" not in result.output:
        pytest.fail('"Usage:" not found in CLI output')
