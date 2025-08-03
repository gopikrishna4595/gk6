# File: tests/test_core_additional.py

import pytest
from typer.testing import CliRunner

from gk6.cli import app
from gk6.core import (
    extract_chaining_variables,
    generate_k6_script,
    list_apis,
)

runner = CliRunner()


def test_cli_invalid_file():
    result = runner.invoke(app, ["invalid_file.json"])
    if result.exit_code == 0:
        pytest.fail("Expected non-zero exit code for invalid file")
    if "Error" not in result.output:
        pytest.fail('"Error" not found in CLI output')


def test_generate_k6_script_with_chaining():
    postman_sample = {
        "item": [
            {
                "name": "Login",
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "exec": ["pm.environment.set('authToken', 'abc123');"]
                        },
                    }
                ],
                "request": {
                    "method": "POST",
                    "url": {"raw": "https://example.com/login"},
                },
            }
        ]
    }
    apis = list_apis(postman_sample)
    script = generate_k6_script(apis, postman_sample)
    if "authToken" not in script:
        pytest.fail("'authToken' not found in generated script")
    if "export default function" not in script:
        pytest.fail("'export default function' not found in generated script")


def test_extract_chaining_variables_multiple():
    postman_sample = {
        "item": [
            {
                "name": "Step1",
                "event": [
                    {
                        "listen": "test",
                        "script": {"exec": ["pm.environment.set('token', '123');"]},
                    }
                ],
            },
            {
                "name": "Step2",
                "event": [
                    {
                        "listen": "test",
                        "script": {"exec": ["pm.environment.set('session', '456');"]},
                    }
                ],
            },
        ]
    }
    chaining_vars = extract_chaining_variables(postman_sample)
    if "token" not in chaining_vars:
        pytest.fail("'token' not found in extracted chaining_vars")
    if "session" not in chaining_vars:
        pytest.fail("'session' not found in extracted chaining_vars")


def test_cli_env_file_option(tmp_path):
    dummy_postman = tmp_path / "collection.json"
    dummy_postman.write_text('{"item": []}')
    dummy_env = tmp_path / "env.json"
    dummy_env.write_text("{}")  # create an empty env file

    result = runner.invoke(
        app,
        [
            "convert",
            "--collection",
            str(dummy_postman),
            "--env",
            str(dummy_env),
            "--all",
        ],
    )
    if result.exit_code != 0:
        print("OUTPUT:", result.output)
        pytest.fail(f"Expected exit code 0, got {result.exit_code}")
