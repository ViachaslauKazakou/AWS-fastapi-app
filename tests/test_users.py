from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 201
    assert response.json() == {"username": "testuser", "email": "test@example.com"}

def test_get_user():
    response = client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "email": "test@example.com"}