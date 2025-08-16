"""
Inverse Design Stub:
Random search over simple controllable parameters to maximize predicted Tg from a trained model.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List

import joblib
import numpy as np
import pandas as pd


@dataclass
class InverseConfig:
    run_dir: str
    n_candidates: int
    features: List[str]
    out_json: str


def propose_candidates(cfg: InverseConfig) -> str:
    model_path = os.path.join(cfg.run_dir, "model.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(model_path)
    model = joblib.load(model_path)

    rng = np.random.default_rng(42)
    cand_rows: List[Dict] = []
    for _ in range(cfg.n_candidates):
        row = {
            "Mw": float(rng.uniform(6e4, 2e5)),
            "Mn": float(rng.uniform(4e4, 1.5e5)),
            "dispersity": float(rng.uniform(1.2, 3.0)),
            "composition_entropy": float(rng.uniform(0.0, 0.7)),
            "bigsmiles_len": int(rng.integers(20, 120)),
            "cooling_rate_K_per_min": float(rng.uniform(1.0, 30.0)),
            "anneal_temperature_C": float(rng.uniform(25, 150)),
            "anneal_time_min": float(rng.uniform(0, 120)),
        }
        X = pd.DataFrame([row])[cfg.features]
        row["pred_Tg_C"] = float(model.predict(X)[0])
        cand_rows.append(row)

    cand_rows.sort(key=lambda r: r["pred_Tg_C"], reverse=True)
    os.makedirs(os.path.dirname(cfg.out_json), exist_ok=True)
    with open(cfg.out_json, "w", encoding="utf-8") as f:
        json.dump(cand_rows, f, indent=2)
    return cfg.out_json
