import pytest

from gk6.core import list_apis


def test_invalid_postman_structure():
    with pytest.raises(KeyError):
        list_apis({"invalid": []})
