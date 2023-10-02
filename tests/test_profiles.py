from sample_data import user_for_profile_1
from test_helpers import check_object

profile_keys = ["username", "bio", "image", "following"]

headers = {"Authorization": None}


def test_user_profile_anonymous(profile_test_client):
    request, response = profile_test_client.get("/api/profiles/Jacob")
    assert response.status == 200
    assert "profile" in response.json
    body = response.json
    assert check_object("profile", profile_keys, response=response.json) == True
    assert body["profile"]["username"] == "Jacob"
    # We will not be following the user here
    assert body["profile"]["following"] == False


def test_follow(profile_test_client):
    # print(user_for_profile_1)
    request, response = profile_test_client.post(
        "/api/users/login", json=user_for_profile_1
    )
    assert response.status == 200
    headers["Authorization"] = f'Token {response.json.get("user").get("token")}'
    request, response = profile_test_client.post(
        "api/profiles/Jacob/follow", headers=headers
    )
    assert response.status == 200
    assert check_object("profile", profile_keys, response=response.json) == True
    assert response.json.get("profile").get("following") == True


def test_unfollow(profile_test_client):
    request, response = profile_test_client.post(
        "/api/users/login", json=user_for_profile_1
    )
    assert response.status == 200
    headers["Authorization"] = f'Token {response.json.get("user").get("token")}'
    request, response = profile_test_client.delete(
        "api/profiles/Jacob/follow", headers=headers
    )
    assert response.status == 200
    assert check_object("profile", profile_keys, response=response.json) == True
    assert response.json.get("profile").get("following") == False
