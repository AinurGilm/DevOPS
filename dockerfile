# 1. Обязательно указываем базовый образ
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем модели (как мы обсуждали)
COPY models/ ./models/

# 6. Копируем остальной код
COPY . .

# 7. Настройка путей для тестов
ENV PYTHONPATH=/app

# 8. Запуск тестов
RUN pytest tests/

# 9. Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]