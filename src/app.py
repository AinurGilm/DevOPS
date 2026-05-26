import os
import joblib
from pathlib import Path

# Получаем путь к папке, где лежит этот файл (src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Теперь путь к моделям всегда будет /app/models/
model_path = BASE_DIR / "models" / "model.pkl"
encoders_path = BASE_DIR / "models" / "encoders.pkl"
features_path = BASE_DIR / "models" / "feature_names.pkl"

try:
    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    feature_names = joblib.load(features_path)
except Exception as e:
    print(f"Ошибка загрузки моделей: {e}")
    # Для тестов можно задать заглушки, чтобы сборка не падала
    model = None
    encoders = {}
    feature_names = []
    
# Pydantic модель должна повторять список колонок, но без пробелов (или с ними)
# ВАЖНО: Ключи должны совпадать по смыслу с вашим CSV
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

@app.post("/predict")
def predict(item: PatientData):
    try:
        data_dict = item.dict()
        df = pd.DataFrame([data_dict])
        
        # Приводим имена к виду CSV (пробелы вместо подчеркиваний)
        df.columns = [c.replace('_', ' ') for c in df.columns]
        
        # Кодируем
        for col, le in encoders.items():
            df[col] = le.transform(df[col])
        
        # СТРОГИЙ ПОРЯДОК:
        df = df[feature_names]
        
        prediction = model.predict(df)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка: {str(e)}")