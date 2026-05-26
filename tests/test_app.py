import pytest
from fastapi.testclient import TestClient
# Импортируем ваше FastAPI приложение
from src.app import app 

client = TestClient(app)

def test_health_endpoint():
    """Проверяем, что сервис в принципе жив"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_prediction_endpoint():
    """Проверяем, что модель принимает новые параметры и выдает прогноз"""
    test_data = {
        "Age": 25,
        "Gender": 1,
        "Current Weight (lbs)": 180.0,
        "BMR (Calories)": 1750,
        "Daily Calories Consumed": 1500,
        "Daily Caloric Surplus/Deficit": -250,
        "Duration (weeks)": 4,
        "Physical Activity Level": 2,
        "Carbs_Pct": 40,
        "Protein_Pct": 30,
        "Fat_Pct": 30,
        "Sleep Quality": 3,
        "Stress Level": 5
    }
    response = client.post("/predict", json=test_data)
    
    # Тест пройдет, если сервер ответит 200 и в JSON будет ключ с прогнозом
    assert response.status_code == 200
    assert "predicted_weight_change_lbs" in response.json()