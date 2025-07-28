# File: gk6/tests/test_cli.py

import subprocess  # nosec B404

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


def test_cli_runs():
    result = subprocess.run(
        ["python", "-m", "gk6.cli", "--help"], capture_output=True, text=True
    )  # nosec B607 B603
    if result.returncode != 0:
        pytest.fail(f"CLI did not run successfully: {result.stderr}")
    if "Usage:" not in result.stdout:
        pytest.fail('"Usage:" not found in CLI output')
