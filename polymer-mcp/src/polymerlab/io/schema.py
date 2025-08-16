"""
JSON Schema loading and validation for MCP Polymer records.
"""
from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Tuple

import yaml
from jsonschema import Draft202012Validator


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def iter_records(paths: Iterable[str]) -> Iterable[Tuple[str, Dict[str, Any]]]:
    """Yield (path, record) for JSON or YAML files."""
    for p in paths:
        if p.endswith((".json", ".JSON")):
            yield p, load_json(p)
        elif p.endswith((".yml", ".yaml", ".YAML", ".YML")):
            yield p, load_yaml(p)


def build_validator(schema_path: str) -> Draft202012Validator:
    schema = load_yaml(schema_path)
    return Draft202012Validator(schema)


def validate_records(validator: Draft202012Validator, records: Iterable[Tuple[str, Dict[str, Any]]]) -> List[str]:
    """
    Validate records; return a list of human-readable error strings (empty if all pass).
    """
    errors: List[str] = []
    for path, rec in records:
        for err in sorted(validator.iter_errors(rec), key=lambda e: e.path):
            loc = " / ".join(map(str, err.path)) or "<root>"
            errors.append(f"{path}: {loc}: {err.message}")
    return errors
