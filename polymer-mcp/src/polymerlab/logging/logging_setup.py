"""
Logging utilities: rotating file logs + JSONL event stream.

* Human-readable rotating log: reports/logs/app.log
* Machine-readable JSONL event stream: reports/logs/events.jsonl
"""
from __future__ import annotations

import json
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

class JsonlHandler(logging.Handler):
    """A simple logging.Handler that writes one JSON object per line."""

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
        ensure_dir(path)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            payload: Dict[str, Any] = {
                "name": record.name,
                "level": record.levelname,
                "msg": record.getMessage(),
                "time": self.formatTime(record),
            }
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
        except Exception:  # pragma: no cover - defensive
            self.handleError(record)

def get_logger(name: str = "polymerlab") -> logging.Logger:
    """Create or retrieve a configured logger."""
    logger = logging.getLogger(name)
    if getattr(logger, "_configured", False):
        return logger

    logger.setLevel(logging.INFO)
    file_path = "reports/logs/app.log"
    ensure_dir(file_path)
    fh = RotatingFileHandler(file_path, maxBytes=2_000_000, backupCount=3)
    fh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(fh)
    jh = JsonlHandler("reports/logs/events.jsonl")
    logger.addHandler(jh)

    logger._configured = True  # type: ignore[attr-defined]
    return logger
