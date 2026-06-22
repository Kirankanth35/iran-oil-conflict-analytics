"""Fetch news attention data from GDELT Doc API.

GDELT's timeline volume mode returns the share of global online news matching a query.
This project uses it as a proxy for media attention to Iran/Hormuz/oil risk.
"""
from __future__ import annotations

import logging
from typing import Dict
from urllib.parse import urlencode

import pandas as pd
import requests

from utils import DATA_RAW, load_config

logger = logging.getLogger(__name__)


def fetch_gdelt_timeline(config: Dict | None = None) -> pd.DataFrame:
    config = config or load_config()
    gdelt = config["gdelt"]
    params = {
        "query": gdelt["query"],
        "mode": gdelt.get("mode", "timelinevol"),
        "format": gdelt.get("format", "json"),
        "startdatetime": gdelt["startdatetime"],
        "enddatetime": gdelt["enddatetime"],
        "timelinesmooth": gdelt.get("timelinesmooth", 3),
    }
    url = f"{gdelt['base_url']}?{urlencode(params)}"
    logger.info("Fetching GDELT timeline volume")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    payload = response.json()

    rows = []
    for series in payload.get("timeline", []):
        for point in series.get("data", []):
            rows.append(point)
    if not rows:
        raise ValueError("No GDELT timeline rows returned. Try broadening the query or dates.")

    df = pd.DataFrame(rows)
    # Common fields include date and value; handle variations defensively.
    date_col = "date" if "date" in df.columns else df.columns[0]
    value_col = "value" if "value" in df.columns else df.columns[-1]
    df = df.rename(columns={date_col: "date", value_col: "gdelt_news_attention"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["gdelt_news_attention"] = pd.to_numeric(df["gdelt_news_attention"], errors="coerce")
    df = df[["date", "gdelt_news_attention"]].dropna().sort_values("date")
    out_path = DATA_RAW / "gdelt_iran_oil_news_attention.csv"
    df.to_csv(out_path, index=False)
    return df


if __name__ == "__main__":
    from utils import ensure_directories, setup_logging

    setup_logging()
    ensure_directories()
    fetch_gdelt_timeline()
