import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_add_review_success():
    response = client.post("/add-review/", data={
        "venue_id": 1,
        "review_title": "Great Place",
        "review_text": "Really enjoyed the atmosphere.",
        "colors": 3,
        "smells": 2,
        "quiet": 4,
        "crowdedness": 1,
        "food_variey": 5,
        "playground": "Yes",
        "fenced": "Yes",
        "quiet_zones": "No",
        "food_own": "No",
        "defined_duration": "Yes"
    }, cookies={"user": "testuser"})
    assert response.status_code == 200
    assert response.json() == {"message": "Review added successfully!"}

def test_add_review_failure():
    response = client.post("/add-review/", data={
        "review_title": "Great Place",
        "review_text": "Really enjoyed the atmosphere.",
        "colors": 3,
        "smells": 2,
        "quiet": 4,
        "crowdedness": 1,
        "food_variey": 5,
        "playground": "Yes",
        "fenced": "Yes",
        "quiet_zones": "No",
        "food_own": "No",
        "defined_duration": "Yes"
    }, cookies={"user": "testuser"})
    assert response.status_code == 422

def test_get_discover():
    response = client.get("/discover")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_api_discover():
    response = client.get("/api/discover")
    assert response.status_code == 200
    assert response.json() == {"venues": []}  # Assuming no venues are in the database

def test_register_user_success():
    response = client.post("/register/", data={
        "nickname": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 303  # Redirect after successful registration

def test_register_user_failure():
    response = client.post("/register/", data={
        "nickname": "",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 422

def test_login_user_success():
    response = client.post("/login/", data={
        "nickname": "testuser",
        "password": "password123"
    })
    assert response.status_code == 303  # Redirect after successful login

def test_login_user_failure():
    response = client.post("/login/", data={
        "nickname": "wronguser",
        "password": "wrongpassword"
    })
    assert response.status_code == 400  # Bad request for wrong credentials

def test_get_welcome():
    response = client.get("/welcome", cookies={"user": "testuser"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_logout_user():
    response = client.get("/logout")
    assert response.status_code == 303  # Redirect after successful logout
