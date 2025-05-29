from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "Test Item", "description": "A test item", "price": 10.0})
    assert response.status_code == 201
    assert response.json() == {"name": "Test Item", "description": "A test item", "price": 10.0}

def test_get_item():
    response = client.get("/items/Test Item")
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item", "description": "A test item", "price": 10.0}