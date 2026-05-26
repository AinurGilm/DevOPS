import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# загрузка данных
data = pd.read_csv("data/data.csv")

# удаляем ID
data = data.drop(columns=["Participant_ID"])

# кодируем текстовые колонки
encoder_gender = LabelEncoder()
encoder_group = LabelEncoder()
encoder_target = LabelEncoder()

data["Gender"] = encoder_gender.fit_transform(data["Gender"])
data["Group"] = encoder_group.fit_transform(data["Group"])

# target
y = encoder_target.fit_transform(data["Dietary_Condition"])

# features
X = data.drop(columns=["Dietary_Condition"])

# split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# модель
model = RandomForestClassifier()

# обучение
model.fit(X_train, y_train)

# создаем папку models
os.makedirs("models", exist_ok=True)

# сохраняем модель
joblib.dump(model, "models/model.pkl")

print("MODEL SAVED")