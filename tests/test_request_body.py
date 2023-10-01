# These sets of requests are only to check whether the validation works if a request is missing the body
# Or the object key


def test_missing_body(test_client):
    request, response = test_client.post("/api/users", json={})
    assert response.status == 422
    assert "errors" in response.json
    assert "message" in response.json["errors"]


def test_validation_errors(test_client):
    request, response = test_client.post("/api/users", json={"user": {}})
    assert response.status == 422
    assert response.json


def test_object_validation_errors(test_client):
    request, response = test_client.post(
        "/api/users", json={"user": {"username": "something"}}
    )
    assert response.status == 422
