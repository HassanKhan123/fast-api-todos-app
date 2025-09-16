from fastapi.testclient import TestClient
from fastapi import status
from ..main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Welcome to the FastAPI application!", "status": "Healthy"}
