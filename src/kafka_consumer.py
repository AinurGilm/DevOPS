"""
Лабораторная работа №4. Kafka Consumer.

Запускается отдельным сервисом в отдельном контейнере (см. docker-compose.yml,
сервис `consumer`, Dockerfile.consumer). Читает сообщения с результатами
инференса и логирует/дублирует их. Обращение к БД (если потребуется
аудит) идёт через защищённые секреты из Vault (см. vault_client.py) —
пароль/адрес БД не хранится в коде consumer'а.
"""
import configparser
import json
import logging
import os
from pathlib import Path

from kafka import KafkaConsumer

from src.vault_client import get_db_credentials

logging.basicConfig(level=logging.INFO, format="%(asctime)s [consumer] %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent


def _load_cfg():
    cfg = configparser.ConfigParser()
    cfg.read(ROOT / "config.ini")
    return cfg["kafka"]


def run() -> None:
    cfg = _load_cfg()
    bootstrap = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", cfg["bootstrap_servers"])
    topic = os.environ.get("KAFKA_TOPIC", cfg["topic_predictions"])
    group_id = os.environ.get("KAFKA_CONSUMER_GROUP", cfg["consumer_group"])

    # Проверяем, что секреты доступны через Vault (защищённое обращение к БД)
    try:
        creds = get_db_credentials()
        log.info("Секреты БД получены из Vault, host=%s", creds["host"])
    except Exception as exc:
        log.warning("Vault недоступен на старте consumer'а: %s", exc)

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    log.info("Consumer запущен, топик=%s, группа=%s", topic, group_id)
    for message in consumer:
        record = message.value
        log.info("Получен результат предсказания: %s", record)


if __name__ == "__main__":
    run()
