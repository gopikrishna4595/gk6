import pytest

from gk6.core import extract_chaining_variables

CHAINED = {
    "item": [
        {
            "event": [
                {
                    "listen": "test",
                    "script": {"exec": ["pm.environment.set('token', '123')"]},
                }
            ]
        }
    ]
}


def test_extract_chaining_variables():
    vars_ = extract_chaining_variables(CHAINED)
    if "token" not in vars_:
        pytest.fail("'token' not found in extracted variables")
