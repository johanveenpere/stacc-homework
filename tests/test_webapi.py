from fastapi.testclient import TestClient
from src.webapi import app

client = TestClient(app)


def test_read_item():
    response = client.get("/iris/1")
    assert response.status_code == 200
