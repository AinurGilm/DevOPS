import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Путь к корню проекта

BASE_DIR = Path(**file**).resolve().parent.parent

# Пути к моделям

model_path = BASE_DIR / "models" / "model.pkl"
encoders_path = BASE_DIR / "models" / "encoders.pkl"
features_path = BASE_DIR / "models" / "feature_names.pkl"

# Загрузка моделей

try:
model = joblib.load(model_path)
encoders = joblib.load(encoders_path)
feature_names = joblib.load(features_path)
except Exception as e:
print(f"Ошибка загрузки моделей: {e}")

```
# Заглушки, чтобы приложение могло импортироваться,
# даже если файлы моделей отсутствуют
model = None
encoders = {}
feature_names = []
```

class PatientData(BaseModel):
Age: float
Gender: str
Current_Weight_lbs: float
BMR_Calories: float
Daily_Calories_Consumed: float
Daily_Caloric_Surplus_Deficit: float
Weight_Change_lbs: float
Duration_weeks: float
Sleep_Quality: str
Stress_Level: str
Final_Weight_lbs: float

@app.get("/")
def home():
return {"status": "OK"}

@app.post("/predict")
def predict(item: PatientData):
try:
if model is None:
raise RuntimeError("Модель не загружена")

```
    data_dict = item.model_dump()
    df = pd.DataFrame([data_dict])

    # Приводим имена колонок к формату CSV
    df.columns = [column.replace("_", " ") for column in df.columns]

    # Кодируем категориальные признаки
    for col, le in encoders.items():
        df[col] = le.transform(df[col])

    # Соблюдаем порядок признаков модели
    df = df[feature_names]

    prediction = model.predict(df)

    return {"prediction": int(prediction[0])}

except Exception as e:
    raise HTTPException(
        status_code=400,
        detail=f"Ошибка: {str(e)}",
    )
```
