"""Deterministic file input/output helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def write_immutable_json(path: Path, payload: Any) -> bool:
    """Write a raw snapshot once and return whether a new file was created."""

    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    return True


def read_json(path: Path) -> Any:
    """Read a UTF-8 JSON file."""

    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(frame: pd.DataFrame, path: Path, sort_by: list[str] | None = None) -> None:
    """Write a stable UTF-8 CSV, optionally sorted by explicit keys."""

    path.parent.mkdir(parents=True, exist_ok=True)
    output = frame.sort_values(sort_by, kind="stable") if sort_by else frame
    output.to_csv(path, index=False, lineterminator="\n")

