"""
API-сервис модели.

ЛР№1: эндпоинт /predict, /health.
ЛР№2: результат сохраняется в PostgreSQL (src/db.py).
ЛР№3: параметры подключения к БД берутся из Vault (src/vault_client.py),
       без хардкода в коде и без локальных конфигов с секретами.
ЛР№4: после сохранения результат публикуется в Kafka (src/kafka_producer.py).
"""
import configparser
import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist

from src.model import predict as model_predict
from src import db

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("api")

ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="Breast Cancer Classifier API")


class PredictRequest(BaseModel):
    features: conlist(float, min_length=30, max_length=30)


class PredictResponse(BaseModel):
    id: int | None
    prediction: int
    probability: List[float]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        result = model_predict(req.features)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    record_id = None
    try:
        record_id = db.save_prediction(
            req.features, result["prediction"], result["probability"]
        )
    except Exception as exc:
        log.warning("Не удалось сохранить результат в БД: %s", exc)

    try:
        from src.kafka_producer import publish_prediction

        publish_prediction(
            record_id or -1, req.features, result["prediction"], result["probability"]
        )
    except Exception as exc:
        log.warning("Не удалось опубликовать результат в Kafka: %s", exc)

    return {
        "id": record_id,
        "prediction": result["prediction"],
        "probability": result["probability"],
    }
