import pytest

from gk6.core import generate_k6_script


def test_generated_script_structure():
    apis = [{"name": "Ping", "method": "GET", "url": "https://example.com/ping"}]
    dummy_postman = {
        "item": [
            {
                "name": "Ping",
                "request": {
                    "method": "GET",
                    "url": {"raw": "https://example.com/ping"},
                },
            }
        ]
    }
    script = generate_k6_script(apis, dummy_postman)

    if "export default function" not in script:
        pytest.fail("K6 script structure invalid")
