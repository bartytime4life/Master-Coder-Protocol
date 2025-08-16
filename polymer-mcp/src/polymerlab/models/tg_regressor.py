"""
Tg regression model with scikit-learn and simple train/test split.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from polymerlab.logging.logging_setup import get_logger


@dataclass
class TrainConfig:
    processed_csv: str
    features: List[str]
    target: str
    test_size: float
    random_state: int
    save_dir: str
    rf_params: Dict


def train(config: TrainConfig) -> Tuple[RandomForestRegressor, Dict[str, float]]:
    logger = get_logger(__name__)
    os.makedirs(config.save_dir, exist_ok=True)

    df = pd.read_csv(config.processed_csv)
    df = df.dropna(subset=[config.target])
    X = df[config.features].fillna(df[config.features].median(numeric_only=True))
    y = df[config.target].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.test_size, random_state=config.random_state
    )

    model = RandomForestRegressor(**config.rf_params)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "r2": float(r2_score(y_test, preds)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, preds))),
        "mae": float(mean_absolute_error(y_test, preds)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }

    joblib.dump(model, os.path.join(config.save_dir, "model.joblib"))
    with open(os.path.join(config.save_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    logger.info(f"Saved model to {config.save_dir}, metrics={metrics}")
    return model, metrics
