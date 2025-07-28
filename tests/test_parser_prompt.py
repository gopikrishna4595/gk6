import pytest

from gk6.core import list_apis

POSTMAN_SAMPLE = {
    "item": [
        {
            "name": "Health Check",
            "request": {"method": "GET", "url": {"raw": "https://example.com/ping"}},
        }
    ]
}


def test_list_apis_extracts_apis():
    apis = list_apis(POSTMAN_SAMPLE)
    if len(apis) != 1:
        pytest.fail("Expected exactly 1 API extracted")
    if apis[0]["method"] != "GET":
        pytest.fail("Expected API method to be 'GET'")
