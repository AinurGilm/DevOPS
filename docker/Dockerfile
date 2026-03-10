FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.ini .
COPY src ./src

# Обучаем модель на этапе сборки образа, чтобы контейнер запускался
# сразу готовым к инференсу (воспроизводимость - фиксированный random_state)
RUN python -m src.data_prep && python -m src.train

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
