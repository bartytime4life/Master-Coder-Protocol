"""
Inductive conformal prediction for regression using residual quantiles.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from polymerlab.logging.logging_setup import get_logger


@dataclass
class ConformalConfig:
    processed_csv: str
    features: List[str]
    target: str
    run_dir: str
    alpha: float
    random_state: int


def fit_conformal(cfg: ConformalConfig) -> Dict:
    """
    Fits a simple conformal interval based on calibration residual quantile.
    Uses the trained model at cfg.run_dir/model.joblib and a held-out split.
    """
    logger = get_logger(__name__)
    model_path = os.path.join(cfg.run_dir, "model.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(model_path)
    model = joblib.load(model_path)

    df = pd.read_csv(cfg.processed_csv).dropna(subset=[cfg.target])
    X = df[cfg.features].fillna(df[cfg.features].median(numeric_only=True))
    y = df[cfg.target].astype(float)

    _, X_cal, _, y_cal = train_test_split(
        X, y, test_size=0.3, random_state=cfg.random_state
    )
    y_pred = model.predict(X_cal)
    resid = np.abs(y_cal - y_pred)
    q = float(np.quantile(resid, 1 - cfg.alpha))
    results = {"alpha": cfg.alpha, "quantile": q}

    with open(os.path.join(cfg.run_dir, "conformal.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Conformal interval radius (q)={q} at alpha={cfg.alpha}")
    return results
