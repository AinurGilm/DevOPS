import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

model_path = BASE_DIR / "models" / "model.pkl"
encoders_path = BASE_DIR / "models" / "encoders.pkl"
features_path = BASE_DIR / "models" / "feature_names.pkl"

model = None
encoders = {}
feature_names = []

if model_path.exists():
model = joblib.load(model_path)

if encoders_path.exists():
encoders = joblib.load(encoders_path)

if features_path.exists():
feature_names = joblib.load(features_path)

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

    df.columns = [
        column.replace("_", " ")
        for column in df.columns
    ]

    for col, encoder in encoders.items():
        df[col] = encoder.transform(df[col])

    if feature_names:
        df = df[feature_names]

    prediction = model.predict(df)

    return {"prediction": int(prediction[0])}

except Exception as e:
    raise HTTPException(
        status_code=400,
        detail=f"Ошибка: {str(e)}",
    )
```
