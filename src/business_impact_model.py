"""Business analytics layer: translate macro-energy risk into decision use cases.

This module is deliberately business-oriented for a GitHub portfolio. It converts
technical indicators into executive-friendly risk scores that can be used in a
BI dashboard, retail/streaming strategy memo, or risk monitoring report.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from utils import DATA_PROCESSED


def _zscore(series: pd.Series) -> pd.Series:
    return (series - series.mean()) / series.std(ddof=0)


def build_business_risk_index() -> pd.DataFrame:
    df = pd.read_csv(DATA_PROCESSED / "master_timeseries.csv", parse_dates=["date"])
    components = []
    if "DCOILWTICO_return" in df:
        df["oil_shock_score"] = _zscore(df["DCOILWTICO_return"].rolling(7).mean()).fillna(0)
        components.append("oil_shock_score")
    if "GASREGW_change" in df:
        df["consumer_fuel_pressure_score"] = _zscore(df["GASREGW_change"].rolling(14).mean()).fillna(0)
        components.append("consumer_fuel_pressure_score")
    if "VIXCLS_change" in df:
        df["market_volatility_score"] = _zscore(df["VIXCLS_change"].rolling(7).mean()).fillna(0)
        components.append("market_volatility_score")
    if "gdelt_news_attention" in df:
        df["geopolitical_attention_score"] = _zscore(df["gdelt_news_attention"].rolling(7).mean()).fillna(0)
        components.append("geopolitical_attention_score")

    if not components:
        raise ValueError("No components available to build business risk index.")

    df["business_risk_index"] = df[components].mean(axis=1)
    df["risk_level"] = pd.cut(
        df["business_risk_index"],
        bins=[-np.inf, -0.5, 0.5, 1.5, np.inf],
        labels=["Low", "Normal", "Elevated", "High"],
    )
    out = df[["date", *components, "business_risk_index", "risk_level"]]
    out.to_csv(DATA_PROCESSED / "business_risk_index.csv", index=False)
    return out


if __name__ == "__main__":
    build_business_risk_index()
