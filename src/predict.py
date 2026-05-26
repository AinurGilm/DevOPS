import joblib
import pandas as pd

model = joblib.load("models/model.pkl")
encoders = joblib.load("models/encoders.pkl")
features = joblib.load("models/feature_names.pkl")

# Пример данных должен содержать ключи из features
sample_data = {
    "Age": 25, "Gender": "Male", "Current Weight (lbs)": 180, 
    "BMR (Calories)": 2000, "Daily Calories Consumed": 2200, 
    "Daily Caloric Surplus/Deficit": 200, "Weight Change (lbs)": 0.5, 
    "Duration (weeks)": 4, "Sleep Quality": "Good", 
    "Stress Level": "Low", "Final Weight (lbs)": 182
}

df = pd.DataFrame([sample_data])
for col, le in encoders.items():
    df[col] = le.transform(df[col])

df = df[features]
print("Prediction:", model.predict(df))