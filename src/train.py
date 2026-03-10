"""
Лабораторная работа №1. Обучение модели.

Гиперпараметры читаются из config.ini, что позволяет менять их
без изменения кода. Результат — сериализованная модель (models/model.joblib)
и метрики (models/metrics.json), которые далее используются в отчёте
и в dev_sec_ops.yml.
"""
import configparser
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODELS_DIR = ROOT / "models"


def load_config() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(ROOT / "config.ini")
    return cfg


def train() -> None:
    cfg = load_config()["model"]

    train_df = pd.read_csv(DATA_DIR / "train.csv")
    test_df = pd.read_csv(DATA_DIR / "test.csv")

    X_train, y_train = train_df.drop(columns=["target"]), train_df["target"]
    X_test, y_test = test_df.drop(columns=["target"]), test_df["target"]

    model = RandomForestClassifier(
        n_estimators=cfg.getint("n_estimators", 200),
        max_depth=cfg.getint("max_depth", 6),
        random_state=cfg.getint("random_state", 42),
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "n_features": X_train.shape[1],
        "feature_names": list(X_train.columns),
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "model.joblib")
    with open(MODELS_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print("Метрики модели:", metrics)


if __name__ == "__main__":
    train()
