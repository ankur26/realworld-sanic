from sample_data import create_users, single_user, updated_user
from sanic import Request, response
from test_helpers import check_object

user_keys = ["email", "token", "username", "bio", "image", "token", "id"]

headers = {
    "Authorization": None
}  # this will change as we gradually progress in the test
token = None


def test_basic_route(test_client):
    request, response = test_client.get("/")
    assert response.status == 200


def test_create_users(test_client):
    for user in create_users:
        request, response = test_client.post("/api/users", json={"user": user})
        assert response.status == 200
        assert check_object("user", user_keys, response=response.json) == True
        assert response.json["user"]["email"] == user["email"]


def test_login(test_client):
    request, response = test_client.post("/api/users/login", json=single_user)
    assert response.status == 200
    body = response.json
    assert (
        check_object("user", user_keys, response=response.json) == True
    )  # will confirm login this time
    # validate the email to confirm that it is it the right user
    assert body["user"]["email"] == single_user["user"]["email"]
    # just store the token to get a user for the next few tests
    token = body["user"]["token"]
    headers["Authorization"] = f'Token {body["user"]["token"]}'


def test_missing_authorization_header(test_client):
    request, response = test_client.get("/api/user")
    assert response.status == 401
    assert "errors" in response.json
    assert "message" in response.json.get("errors")


def test_missing_bearer_prefix(test_client):
    # just send the token as is it is to check this
    # print(headers)

    request, response = test_client.get("api/user", headers={"Authorization": ""})
    assert response.status == 401
    assert "errors" in response.json
    assert "message" in response.json.get("errors")


def test_get_user(test_client):
    request, response = test_client.get("/api/user", headers=headers)
    print(request.headers)
    assert response.status == 200
    body = response.json
    assert body["user"]["email"] == single_user["user"]["email"]


def test_update_user(test_client):
    request, response = test_client.put("/api/user", headers=headers, json=updated_user)

    print(request.headers)
    assert response.status == 200
    assert "user" in response.json
    assert "email" in response.json.get("user")
    assert response.json.get("user").get("email") == updated_user["user"]["email"]
