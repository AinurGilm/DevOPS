"""
Лабораторная работа №4. Kafka Producer.

Реализован на уровне сервиса модели: после инференса результат
отправляется в топик Kafka, откуда его забирает отдельный
Consumer-сервис (см. kafka_consumer.py, запускается своим контейнером).
"""
import configparser
import json
import os
from pathlib import Path

from kafka import KafkaProducer

ROOT = Path(__file__).resolve().parent.parent
_producer = None


def _load_cfg():
    cfg = configparser.ConfigParser()
    cfg.read(ROOT / "config.ini")
    return cfg["kafka"]


def get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        cfg = _load_cfg()
        bootstrap = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", cfg["bootstrap_servers"])
        _producer = KafkaProducer(
            bootstrap_servers=bootstrap,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
        )
    return _producer


def publish_prediction(record_id: int, features: list, prediction: int, probability: list) -> None:
    cfg = _load_cfg()
    topic = os.environ.get("KAFKA_TOPIC", cfg["topic_predictions"])
    message = {
        "id": record_id,
        "features": features,
        "prediction": prediction,
        "probability": probability,
    }
    producer = get_producer()
    producer.send(topic, value=message)
    producer.flush()
