"""
Physics rule checks for processed CSV rows, using expressions defined in a rules YAML.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List

import pandas as pd
import yaml


@dataclass
class Rule:
    name: str
    rule_expr: str
    severity: str


def load_rules(path: str) -> List[Rule]:
    spec = yaml.safe_load(open(path, "r", encoding="utf-8"))
    checks = spec.get("checks", {}) or {}
    rules: List[Rule] = []
    for name, body in checks.items():
        rules.append(Rule(name=name, rule_expr=str(body.get("rule", "true")), severity=str(body.get("severity", "warn"))))
    return rules


def evaluate_rules(df: pd.DataFrame, rules: List[Rule]) -> pd.DataFrame:
    """
    Evaluate simple boolean expressions in the context of each row.
    Exposes row fields as variables by their column names.
    """
    records: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        env = {k: (None if (isinstance(v, float) and math.isnan(v)) else v) for k, v in row.to_dict().items()}
        row_id = env.get("polymer_id", None)
        for r in rules:
            try:
                ok = bool(eval(r.rule_expr, {"__builtins__": {}}, env))
            except Exception:
                ok = False
            if not ok:
                records.append({"polymer_id": row_id, "rule": r.name, "severity": r.severity, "ok": ok})
    return pd.DataFrame.from_records(records)
