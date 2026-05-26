FROM python:3.11-slim

# ... ваши инструкции установки ...
WORKDIR /app

# Добавьте эту строку перед запуском тестов
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Теперь pytest найдет модуль src
RUN pytest tests/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]