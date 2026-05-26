WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем модели в /app/models/
COPY models/ ./models/ 

# Копируем остальной код
COPY . .

# Устанавливаем PYTHONPATH, чтобы импорты из src работали
ENV PYTHONPATH=/app

# Запуск тестов
RUN pytest tests/