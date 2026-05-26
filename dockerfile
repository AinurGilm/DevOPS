FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта и тесты
COPY . .

ENV PYTHONPATH=/app

# --- ЭТАП АВТОТЕСТОВ ПРЯМО ПРИ СБОРКЕ ОБРАЗА ---
# Если тесты упадут, Docker-образ не соберётся, и пайплайн Jenkins прервется
RUN pytest tests/

# Команда для запуска приложения на продакшене
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]