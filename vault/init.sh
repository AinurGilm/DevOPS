#!/bin/sh
# Лабораторная работа №3.
# Инициализация хранилища секретов на этапе старта окружения (docker-compose
# сервис vault-init). Хардкод dev-параметров здесь допустим согласно заданию
# ("допускается хардкод параметров и добавление их в .gitignore") -
# реальные значения переопределяются файлом vault/secrets.env, который
# НЕ коммитится в репозиторий (см. .gitignore), в репозитории только
# vault/secrets.env.example.

set -e

export VAULT_ADDR="http://vault:8200"
export VAULT_TOKEN="${VAULT_DEV_ROOT_TOKEN:-root-dev-token}"

# Ждём, пока Vault поднимется
until vault status >/dev/null 2>&1; do
  echo "Ожидание запуска Vault..."
  sleep 2
done

# Включаем KV v2 (в dev-режиме уже включено по умолчанию как secret/, но
# на случай не-dev режима - явное включение идемпотентно)
vault secrets enable -path=secret -version=2 kv || true

vault kv put secret/db-credentials \
  host="${DB_HOST:-postgres}" \
  port="${DB_PORT:-5432}" \
  dbname="${DB_NAME:-ml_lab}" \
  user="${DB_USER:-ml_user}" \
  password="${DB_PASSWORD:-change_me_in_secrets_env}"

echo "Секреты БД успешно размещены в Vault (secret/db-credentials)"
