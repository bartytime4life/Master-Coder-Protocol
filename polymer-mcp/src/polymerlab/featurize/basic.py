"""
Basic featurization from MCP Polymer records into a tabular DataFrame suitable for ML.

Features:
* Mw, Mn, dispersity (if present)
* BigSMILES string length as a cheap proxy
* Composition entropy over monomer fractions
* Processing: cooling_rate_K_per_min, anneal temperature/time
Target (default): Tg_C if available
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


def composition_entropy(comp: Optional[List[Dict[str, Any]]]) -> float:
    """Shannon entropy over composition fractions; 0 if absent."""
    if not comp:
        return 0.0
    p = np.array([max(1e-12, float(c.get("fraction", 0.0))) for c in comp], dtype=float)
    p = p / p.sum()
    return float(-(p * np.log(p)).sum())


def extract_row(path: str, rec: Dict[str, Any]) -> Dict[str, Any]:
    iden = rec.get("identity", {})
    mw = rec.get("molecular_weight", {}) or {}
    proc = rec.get("processing", {}) or {}
    anneal = proc.get("anneal", {}) or {}
    props = rec.get("properties", {}) or {}

    row: Dict[str, Any] = {
        "path": path,
        "polymer_id": rec.get("polymer_id"),
        "bigsmiles_len": len((iden.get("bigsmiles") or "")),
        "composition_entropy": composition_entropy(iden.get("composition")),
        "Mw": float(mw.get("Mw")) if mw.get("Mw") is not None else np.nan,
        "Mn": float(mw.get("Mn")) if mw.get("Mn") is not None else np.nan,
        "dispersity": float(mw.get("dispersity")) if mw.get("dispersity") is not None else np.nan,
        "cooling_rate_K_per_min": float(proc.get("cooling_rate_K_per_min")) if proc.get("cooling_rate_K_per_min") is not None else np.nan,
        "anneal_temperature_C": float(anneal.get("temperature_C")) if anneal.get("temperature_C") is not None else np.nan,
        "anneal_time_min": float(anneal.get("time_min")) if anneal.get("time_min") is not None else np.nan,
        "Tg_C": float(props.get("Tg_C")) if props.get("Tg_C") is not None else np.nan,
        "Tm_C": float(props.get("Tm_C")) if props.get("Tm_C") is not None else np.nan,
    }
    return row


def to_dataframe(records: Iterable[Tuple[str, Dict[str, Any]]]) -> pd.DataFrame:
    rows = [extract_row(p, r) for p, r in records]
    df = pd.DataFrame(rows)
    front = ["polymer_id", "path", "bigsmiles_len", "composition_entropy", "Mw", "Mn", "dispersity",
             "cooling_rate_K_per_min", "anneal_temperature_C", "anneal_time_min", "Tg_C", "Tm_C"]
    rest = [c for c in df.columns if c not in front]
    return df[front + rest]
