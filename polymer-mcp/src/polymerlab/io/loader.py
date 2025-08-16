"""
Data loading helpers for raw/interim/processed flows.
"""
from __future__ import annotations

import glob
import os
from typing import List


def glob_files(patterns: List[str]) -> List[str]:
    paths: List[str] = []
    for pat in patterns:
        paths.extend(glob.glob(pat))
    return [p for p in paths if os.path.isfile(p)]
