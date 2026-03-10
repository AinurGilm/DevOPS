"""
Лабораторная работа №1. Этап подготовки данных.

Используется встроенный в scikit-learn датасет Breast Cancer Wisconsin
(эквивалент https://www.kaggle.com/uciml/breast-cancer-wisconsin-data),
что позволяет не тянуть данные из внешних источников на этапе сборки
контейнера и делает пайплайн полностью воспроизводимым.
"""
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def prepare_data(test_size: float = 0.2, random_state: int = 42) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_breast_cancer(as_frame=True)
    df = dataset.frame  # признаки + столбец target

    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state, stratify=df["target"]
    )

    train_df.to_csv(DATA_DIR / "train.csv", index=False)
    test_df.to_csv(DATA_DIR / "test.csv", index=False)

    print(f"train: {train_df.shape}, test: {test_df.shape}")
    print(f"файлы сохранены в {DATA_DIR}")


if __name__ == "__main__":
    prepare_data()
