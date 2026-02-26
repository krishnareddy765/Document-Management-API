from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():
    response = client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    assert response.status_code == 200


def test_login():
    response = client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    assert response.status_code == 200