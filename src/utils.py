"""Utility functions for the U.S.-Iran oil conflict analytics project."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "config.yaml"
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"
MAPS = ROOT / "reports" / "maps"


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_directories() -> None:
    for p in [DATA_RAW, DATA_PROCESSED, FIGURES, MAPS]:
        p.mkdir(parents=True, exist_ok=True)


def parse_float(value: Any) -> float | None:
    try:
        if value in [".", "", None, "NA"]:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None
