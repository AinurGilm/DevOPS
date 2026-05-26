import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# 1. Загрузка данных
data = pd.read_csv("data/data.csv")
if 'Participant ID' in data.columns:
    data = data.drop(columns=['Participant ID'])

target_col = 'Physical Activity Level'
encoder_target = LabelEncoder()
y = encoder_target.fit_transform(data[target_col])
X = data.drop(columns=[target_col])

# 2. Кодирование
encoders = {}
for col in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

# 3. Сохраняем порядок колонок
feature_names = X.columns.tolist()

# 4. Обучение
model = RandomForestClassifier()
model.fit(X, y)

# 5. Сохранение
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.pkl")
joblib.dump(encoders, "models/encoders.pkl")
joblib.dump(feature_names, "models/feature_names.pkl") # ВАЖНО

print("Модель обучена. Признаки:", feature_names)