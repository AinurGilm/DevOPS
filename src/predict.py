import joblib
import pandas as pd

# загрузка модели
model = joblib.load("models/model.pkl")

# пример данных
sample = pd.DataFrame([{
    "Age": 25,
    "Gender": 1,
    "Group": 0,
    "Duration_Weeks": 12,
    "Compliance_Rate": 0.9,
    "Initial_Body_Fat_Pct": 25.0,
    "Final_Body_Fat_Pct": 20.0,
    "Initial_Lean_Mass_kg": 50.0,
    "Final_Lean_Mass_kg": 53.0,
    "VO2_Max_Change_Pct": 10.0
}])

prediction = model.predict(sample)

print("Prediction:", prediction)