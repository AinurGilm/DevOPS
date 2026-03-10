import json
from pathlib import Path

import pytest

from src.data_prep import prepare_data
from src.train import train
from src.model import predict

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module", autouse=True)
def trained_model():
    prepare_data()
    train()
    yield


def test_metrics_file_created():
    metrics_path = ROOT / "models" / "metrics.json"
    assert metrics_path.exists()
    metrics = json.loads(metrics_path.read_text())
    assert metrics["accuracy"] > 0.8


def test_predict_shape():
    features = [0.0] * 30
    result = predict(features)
    assert result["prediction"] in (0, 1)
    assert len(result["probability"]) == 2
