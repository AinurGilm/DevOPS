# Базовый образ
FROM python:3.11-slim

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости первыми для кэширования
COPY requirements.txt .

# Устанавливаем библиотеки (этот слой будет кэшироваться)
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальной код
COPY . .

# Запуск тестов
RUN pytest tests/

# Команда запуска
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]