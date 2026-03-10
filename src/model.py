"""Обёртка над сериализованной моделью для использования в API."""
from pathlib import Path
from typing import List

import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "model.joblib"

_model = None


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Модель не найдена по пути {MODEL_PATH}. "
                "Сначала выполните data_prep.py и train.py."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(features: List[float]) -> dict:
    model = get_model()
    x = np.array(features).reshape(1, -1)
    pred = int(model.predict(x)[0])
    proba = model.predict_proba(x)[0].tolist()
    return {"prediction": pred, "probability": proba}
