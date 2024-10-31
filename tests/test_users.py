import pytest
from jose import jwt
from app import schemas
from app.config import settings


# Test user creation
def test_create_user(client):
    # Send POST request to create a new user
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    # Validate the response
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


# Test user login
def test_login_user(test_user, client):
    # Send POST request to login
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})

    # Validate the login response
    login_res = schemas.Token(**res.json())

    # Decode the JWT token
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    # Assert the decoded user ID matches the test user's ID
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


# Parameterized test for incorrect login attempts
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    # Attempt login with various incorrect credentials
    res = client.post(
        "/login", data={"username": email, "password": password})

    # Assert the expected status code
    assert res.status_code == status_code
    # Note: The following assertion is commented out
    # assert res.json().get('detail') == 'Invalid Credentials'
