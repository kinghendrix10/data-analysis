# tests/test_api_endpoints.py

import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_upload_file():
    file = {"file": open("test.xlsx", "rb")}
    response = client.post("/upload", files=file)
    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"

def test_query_data():
    query = {"query": "Show me the statistics of the data."}
    response = client.post("/query", json=query)
    assert response.status_code == 200
    assert response.json()["response"] is not None
