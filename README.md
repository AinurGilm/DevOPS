# Инфраструктура больших данных — ЛР №1–4

Единый проект классификации (Breast Cancer Wisconsin), который поэтапно
обрастает инфраструктурой: ЛР№1 (жизненный цикл модели) → ЛР№2 (PostgreSQL)
→ ЛР№3 (HashiCorp Vault) → ЛР№4 (Apache Kafka).

История коммитов в `git log` уже размечена по лабораторным — каждая ЛР —
отдельный коммит поверх предыдущей.

## Структура репозитория

```
src/                  исходный код (модель, API, БД, Vault, Kafka)
tests/                pytest-тесты
docker/               Dockerfile (модель), Dockerfile.consumer
scripts/init.sql      схема PostgreSQL
vault/                init.sh + secrets.env.example (шаблон, без реальных секретов)
.github/workflows/    CI (ci.yml) и CD (cd.yml) на GitHub Actions
docker-compose.yml            финальная версия — весь стек (ЛР№2+3+4)
docker-compose.lab1.yml       чекпоинт: только модель (ЛР№1)
docker-compose.lab2.yml       чекпоинт: модель + Postgres (ЛР№2)
docker-compose.lab3.yml       чекпоинт: модель + Postgres + Vault (ЛР№3)
config.ini, requirements.txt, dev_sec_ops.yml, scenario.json, dvc.yaml
```

## 1. Публикация на GitHub

```bash
unzip ml-infra-lab.zip && cd ml-infra-lab
# репозиторий уже инициализирован (git log покажет 5 коммитов)
git remote add origin https://github.com/<ваш_логин>/ml-infra-lab.git
git branch -M main
git push -u origin main
```

Для повторения логики задания ("создать репозиторий-форк из ЛР№N")
можно создать отдельные ветки/форки на коммитах `Lab1`, `Lab2`, `Lab3`:

```bash
git log --oneline           # найти нужный commit hash
git checkout -b lab2-branch <hash коммита ЛР№2>
```

## 2. Настройка секретов CI/CD (GitHub → Settings → Secrets and variables → Actions)

| Secret               | Значение                                    |
|-----------------------|----------------------------------------------|
| `DOCKERHUB_USERNAME`  | ваш логин на hub.docker.com                   |
| `DOCKERHUB_TOKEN`     | Access Token (Docker Hub → Account Settings → Security) |

## 3. Локальный запуск (все 4 лабораторные сразу)

```bash
cp vault/secrets.env.example vault/secrets.env
# откройте vault/secrets.env и задайте свои значения DB_PASSWORD и др.

docker compose up --build
```

Поднимутся: `postgres`, `vault`, `vault-init`, `zookeeper`, `kafka`,
`model-api`, `consumer`.

Проверка:
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}'
docker compose logs consumer   # убедиться, что сообщение дошло из Kafka
```

Swagger-документация API: http://localhost:8000/docs

Остановка: `docker compose down -v`

## 4. Поэтапный запуск (если нужно продемонстрировать каждую ЛР отдельно)

```bash
# ЛР№1 — только модель
docker compose -f docker-compose.lab1.yml up --build

# ЛР№2 — модель + PostgreSQL
docker compose -f docker-compose.lab2.yml up --build

# ЛР№3 — модель + PostgreSQL + Vault
cp vault/secrets.env.example vault/secrets.env
docker compose -f docker-compose.lab3.yml up --build

# ЛР№4 — полный стек (см. пункт 3 выше, docker-compose.yml)
```

## 5. CI/CD пайплайн

- **CI** (`.github/workflows/ci.yml`): срабатывает на `pull_request` в `main` →
  прогоняет `pytest` → собирает Docker-образы `model-api` и `consumer` →
  пушит их на DockerHub с тегами `<short_sha>` и `latest`.
- **CD** (`.github/workflows/cd.yml`): запускается вручную (`workflow_dispatch`),
  по расписанию (`cron`) или автоматически после успешного CI
  (`workflow_run`) → поднимает `docker compose up -d` → прогоняет
  функциональные проверки по `scenario.json` → гасит стек.

Чтобы увидеть работу пайплайна: сделайте любое небольшое изменение в коде,
закоммитьте в отдельную ветку и откройте Pull Request в `main`.

## 6. DVC (версионирование данных/модели)

```bash
pip install -r requirements.txt
dvc init          # если ещё не инициализирован в этом клоне
dvc repro          # прогонит data_prep -> train, положит метрики в models/metrics.json
```

## 7. Обучение модели вручную (без Docker)

```bash
python -m src.data_prep
python -m src.train
uvicorn src.api:app --reload
```

## 8. Что проверить перед сдачей

- [ ] `git log --oneline` показывает историю по этапам ЛР1→ЛР4
- [ ] Pull Request открыт в `main`, CI прошёл зелёным, образы есть на DockerHub
- [ ] CD-workflow запущен вручную хотя бы раз, шаги scenario.json прошли
- [ ] `vault/secrets.env` НЕ закоммичен (проверить `git status` и `.gitignore`)
- [ ] В README/отчёте указаны ссылки на репозиторий и DockerHub-образ
