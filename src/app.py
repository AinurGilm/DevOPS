from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

# 1. Загружаем модель и энкодеры
# Убедитесь, что пути соответствуют тем, где лежат ваши файлы в контейнере
try:
    model = joblib.load("models/model.pkl")
    encoders = joblib.load("models/encoders.pkl")
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")

# 2. Определяем структуру входящих данных (валидация)
class PatientData(BaseModel):
    Age: float
    Gender: str
    Current_Weight_lbs: float  # Убрали пробелы для удобства программирования
    BMR_Calories: float
    Daily_Calories_Consumed: float
    Daily_Caloric_Surplus_Deficit: float
    Weight_Change_lbs: float
    Duration_weeks: float
    Physical_Activity_Level: str
    Sleep_Quality: str
    Stress_Level: str
    Final_Weight_lbs: float

@app.get("/")
def home():
    return {"status": "ok", "message": "ML Model API is running"}

@app.post("/predict")
def predict(item: PatientData):
    try:
        # Преобразуем входящие данные в DataFrame
        data_dict = item.dict()
        df = pd.DataFrame([data_dict])
        
        # Переименовываем колонки, если есть несовпадения с тем, на чем училась модель
        # Например, меняем подчеркивания на пробелы, если модель ждет их
        df.columns = df.columns.str.replace('_', ' ')
        
        # Кодируем строковые поля через сохраненные энкодеры
        for col, le in encoders.items():
            if col in df.columns:
                df[col] = le.transform(df[col])
        
        # Делаем прогноз
        prediction = model.predict(df)
        
        return {
            "prediction": int(prediction[0])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))