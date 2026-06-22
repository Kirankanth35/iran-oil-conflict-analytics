"""Build the modeling table used for all research questions."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from utils import DATA_RAW, DATA_PROCESSED, load_config

logger = logging.getLogger(__name__)


def _load_raw_fred(series_id: str) -> pd.DataFrame | None:
    path = DATA_RAW / f"fred_{series_id}.csv"
    if not path.exists():
        logger.warning("Missing %s", path)
        return None
    df = pd.read_csv(path)
    if "observation_date" in df.columns:
        df = df.rename(columns={"observation_date": "date"})
    elif "DATE" in df.columns:
        df = df.rename(columns={"DATE": "date"})
    value_col = [c for c in df.columns if c != "date"][0]
    df = df.rename(columns={value_col: series_id})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df[series_id] = pd.to_numeric(df[series_id].replace(".", np.nan), errors="coerce")
    return df.dropna(subset=["date"]).sort_values("date")


def build_master_table(config: Dict | None = None) -> pd.DataFrame:
    config = config or load_config()
    series_ids = list(config["fred"]["series"].keys())

    master: pd.DataFrame | None = None
    for sid in series_ids:
        df = _load_raw_fred(sid)
        if df is None:
            continue
        master = df if master is None else master.merge(df, on="date", how="outer")

    if master is None:
        raise FileNotFoundError("No FRED data found. Run src/fetch_fred.py first.")

    gdelt_path = DATA_RAW / "gdelt_iran_oil_news_attention.csv"
    if gdelt_path.exists():
        gdelt = pd.read_csv(gdelt_path)
        gdelt["date"] = pd.to_datetime(gdelt["date"], errors="coerce")
        master = master.merge(gdelt, on="date", how="left")
    else:
        master["gdelt_news_attention"] = np.nan

    master = master.sort_values("date")
    # Forward-fill weekly/monthly series to daily for aligned modeling.
    non_date_cols = [c for c in master.columns if c != "date"]
    master[non_date_cols] = master[non_date_cols].ffill()

    for col in ["DCOILWTICO", "DCOILBRENTEU", "GASREGW", "SP500", "VIXCLS"]:
        if col in master:
            master[f"{col}_return"] = master[col].pct_change()
            master[f"{col}_change"] = master[col].diff()

    if "DCOILBRENTEU" in master and "DCOILWTICO" in master:
        master["brent_wti_spread"] = master["DCOILBRENTEU"] - master["DCOILWTICO"]

    # Event-period labels
    ew = config["event_windows"]
    pre_end = pd.to_datetime(ew["pre_conflict_end"])
    conflict_start = pd.to_datetime(ew["conflict_start"])
    deesc_start = pd.to_datetime(ew["tentative_deescalation_start"])

    master["period"] = "baseline"
    master.loc[master["date"] <= pre_end, "period"] = "pre_conflict"
    master.loc[(master["date"] >= conflict_start) & (master["date"] < deesc_start), "period"] = "conflict"
    master.loc[master["date"] >= deesc_start, "period"] = "deescalation"

    out_path = DATA_PROCESSED / "master_timeseries.csv"
    master.to_csv(out_path, index=False)
    logger.info("Saved %s", out_path)
    return master


if __name__ == "__main__":
    from utils import ensure_directories, setup_logging

    setup_logging()
    ensure_directories()
    build_master_table()
