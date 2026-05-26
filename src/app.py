from fastapi import FastAPI
import joblib

app = FastAPI()

model = joblib.load("models/model.pkl")

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: list):
    prediction = model.predict([data])

    return {
        "prediction": int(prediction[0])
    }