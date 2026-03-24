"""
Лабораторная работа №2. Взаимодействие с источником данных (PostgreSQL).

В исходном коде НЕТ явно прописанных логина/пароля/адреса БД.
Начиная с лабораторной работы №3 параметры подключения приходят
не из переменных окружения напрямую, а через vault_client.get_db_credentials(),
который забирает секреты из HashiCorp Vault. Для обратной совместимости
(лабораторная №2 без Vault) сохранён fallback на переменные окружения.
"""
import os
from contextlib import contextmanager
from typing import Iterator

import psycopg2
from psycopg2.extensions import connection as PGConnection

try:
    from src.vault_client import get_db_credentials
except Exception:  # Vault ещё не подключен (состояние ЛР№2)
    get_db_credentials = None


def _resolve_credentials() -> dict:
    """Секреты не хардкодятся. Приоритет: Vault -> переменные окружения."""
    if get_db_credentials is not None:
        try:
            return get_db_credentials()
        except Exception:
            pass  # Vault недоступен - используем env (например, локальная отладка)

    return {
        "host": os.environ["DB_HOST"],
        "port": os.environ.get("DB_PORT", "5432"),
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }


@contextmanager
def get_connection() -> Iterator[PGConnection]:
    creds = _resolve_credentials()
    conn = psycopg2.connect(
        host=creds["host"],
        port=creds["port"],
        dbname=creds["dbname"],
        user=creds["user"],
        password=creds["password"],
    )
    try:
        yield conn
    finally:
        conn.close()


def init_schema() -> None:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                features JSONB NOT NULL,
                prediction INTEGER NOT NULL,
                probability JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
        )
        conn.commit()


def save_prediction(features: list, prediction: int, probability: list) -> int:
    import json

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO predictions (features, prediction, probability)
            VALUES (%s, %s, %s) RETURNING id;
            """,
            (json.dumps(features), prediction, json.dumps(probability)),
        )
        row_id = cur.fetchone()[0]
        conn.commit()
        return row_id
