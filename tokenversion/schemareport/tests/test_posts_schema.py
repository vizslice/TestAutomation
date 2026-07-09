import allure
import jsonschema
import pytest
import requests

from conftest import load_schema

POST_SCHEMA = load_schema("post_schema.json")


@allure.feature("Posts")
@allure.story("GET single post matches schema")
@pytest.mark.parametrize("post_id", [1, 2, 3, 10, 20])
def test_get_post_schema(base_url, auth_headers, post_id):
    resp = requests.get(f"{base_url}/posts/{post_id}", headers=auth_headers)
    assert resp.status_code == 200

    with allure.step(f"Validate post {post_id} against post_schema.json"):
        jsonschema.validate(instance=resp.json(), schema=POST_SCHEMA)


@allure.feature("Posts")
@allure.story("POST created post matches schema")
def test_create_post_schema(base_url, auth_headers):
    payload = {"title": "New Post", "body": "Some body text", "userId": 1}
    resp = requests.post(f"{base_url}/posts", json=payload, headers=auth_headers)
    assert resp.status_code == 201

    with allure.step("Validate created post against post_schema.json"):
        jsonschema.validate(instance=resp.json(), schema=POST_SCHEMA)
