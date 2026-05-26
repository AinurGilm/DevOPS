import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# 1. Загрузка данных
data = pd.read_csv("data/data.csv")

# 2. Удаление ID (исправили имя колонки)
if 'Participant ID' in data.columns:
    data = data.drop(columns=['Participant ID'])

# 3. Выбираем целевую колонку (например, 'Physical Activity Level')
target_col = 'Physical Activity Level'
encoder_target = LabelEncoder()
y = encoder_target.fit_transform(data[target_col])

# 4. Удаляем таргет из признаков
X = data.drop(columns=[target_col])

# 5. Автоматическое кодирование ВСЕХ текстовых колонок
# Это исправит вашу ошибку ValueError: 'Good'
encoders = {}
for col in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le # Сохраняем энкодер, чтобы использовать в API

# 6. Обучение
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 7. Сохранение
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.pkl")
joblib.dump(encoders, "models/encoders.pkl") # Сохраняем все энкодеры в один файл

print("MODEL SAVED SUCCESSFULLY")