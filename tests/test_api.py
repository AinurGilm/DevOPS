from fastapi.testclient import TestClient

from src.data_prep import prepare_data
from src.train import train
from src.api import app

prepare_data()
train()

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_predict_endpoint():
    payload = {"features": [0.0] * 30}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "prediction" in body
    assert "probability" in body
