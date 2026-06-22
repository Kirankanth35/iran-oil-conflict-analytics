"""Fetch public macro/energy time series from FRED without an API key."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import pandas as pd
import requests

from utils import DATA_RAW, load_config, parse_float

logger = logging.getLogger(__name__)


def fetch_fred_series(series_id: str, base_url: str, out_dir: Path = DATA_RAW) -> pd.DataFrame:
    """Download a FRED CSV series and save it under data/raw.

    FRED graph CSV URLs are public and usually follow this pattern:
    https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILWTICO
    """
    url = f"{base_url}{series_id}"
    logger.info("Fetching FRED series %s", series_id)
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    out_path = out_dir / f"fred_{series_id}.csv"
    out_path.write_bytes(response.content)

    df = pd.read_csv(out_path)
    if "observation_date" in df.columns:
        df = df.rename(columns={"observation_date": "date"})
    elif "DATE" in df.columns:
        df = df.rename(columns={"DATE": "date"})

    value_col = [c for c in df.columns if c != "date"][0]
    df = df.rename(columns={value_col: series_id})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df[series_id] = df[series_id].map(parse_float)
    df = df.dropna(subset=["date"]).sort_values("date")
    return df


def fetch_all_fred(config: Dict | None = None) -> Dict[str, pd.DataFrame]:
    config = config or load_config()
    base_url = config["fred"]["base_url"]
    series = config["fred"]["series"]
    result = {}
    for series_id in series:
        try:
            result[series_id] = fetch_fred_series(series_id, base_url)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not fetch %s: %s", series_id, exc)
    return result


if __name__ == "__main__":
    from utils import ensure_directories, setup_logging

    setup_logging()
    ensure_directories()
    fetch_all_fred()
