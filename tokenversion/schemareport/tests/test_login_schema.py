import allure
import jsonschema
import requests

from conftest import load_schema


@allure.feature("Auth")
@allure.story("Login response matches schema")
def test_login_schema(base_url):
    resp = requests.post(
        f"{base_url}/login",
        json={"username": "student", "password": "student123"},
    )
    assert resp.status_code == 200

    schema = load_schema("login_schema.json")
    with allure.step("Validate response body against login_schema.json"):
        jsonschema.validate(instance=resp.json(), schema=schema)
