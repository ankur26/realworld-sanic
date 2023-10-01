import pytest
from sample_data import (user_for_profile_1_registration,
                         user_for_profile_2_registration)

from realworld.server import create_app


@pytest.fixture(scope="session")
def test_client():
    app = create_app(test=True)
    return app.test_client


@pytest.fixture(scope="module")
def profile_test_client():
    app = create_app(test=True)
    test_client = app.test_client
    _, response = test_client.post("api/users", json=user_for_profile_1_registration)
    _, response = test_client.post("api/users", json=user_for_profile_2_registration)
    return test_client
