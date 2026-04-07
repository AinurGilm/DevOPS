"""
Лабораторная работа №3. Взаимодействие с хранилищем секретов (HashiCorp Vault).

Секреты (логин/пароль/адрес БД) размещаются в Vault KV-хранилище на этапе
сборки/старта контейнера сервисом `vault-init` (см. docker-compose.yml
и vault/init.sh). Сервис модели НЕ хранит их в файлах конфигурации —
он получает их через HTTP API Vault по адресу и токену, которые
передаются как переменные окружения контейнера (VAULT_ADDR, VAULT_TOKEN).

Локальные .env/config-файлы с реальными секретами не коммитятся
(см. .gitignore), в репозитории остаётся только шаблон .env.example.
"""
import os

import hvac

SECRET_PATH = "secret/data/db-credentials"  # KV v2


def _client() -> hvac.Client:
    addr = os.environ["VAULT_ADDR"]
    token = os.environ["VAULT_TOKEN"]
    client = hvac.Client(url=addr, token=token)
    if not client.is_authenticated():
        raise RuntimeError("Не удалось аутентифицироваться в Vault")
    return client


def get_db_credentials() -> dict:
    client = _client()
    resp = client.secrets.kv.v2.read_secret_version(path="db-credentials")
    data = resp["data"]["data"]
    return {
        "host": data["host"],
        "port": data.get("port", "5432"),
        "dbname": data["dbname"],
        "user": data["user"],
        "password": data["password"],
    }


def get_kafka_credentials() -> dict:
    """Используется в ЛР№4 для защищённого обращения Kafka-сервисов к БД."""
    return get_db_credentials()
