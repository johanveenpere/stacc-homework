import requests
from api import webapi


# Integration test. Requires the containers to be up.
def test_read_item():
    response = requests.get("http://localhost:8000/iris/1")
    assert response.status_code == 200


# Integration test. Requires the containers to be up.
def test_read_all():
    response = requests.get("http://localhost:8000/irises")
    assert response.status_code == 200


# Unit test.
def test_condition_parsing():
    assert webapi.parse_condition("gt6.0") == ">6.0"
    assert webapi.parse_condition("ge6.0") == ">=6.0"
    assert webapi.parse_condition("eq6.0") == "=6.0"
    assert webapi.parse_condition("lt6.0") == "<6.0"
    assert webapi.parse_condition("le6.0") == "<=6.0"
    assert webapi.parse_condition("ne6.0") == "!=6.0"
