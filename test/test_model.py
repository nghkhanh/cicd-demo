import pytest
from fastapi.testclient import TestClient
import os
import sys

from src.app import app, load_model

load_model()

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["status"] == "running"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
