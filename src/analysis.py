"""Statistical analysis for the three research questions."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from utils import DATA_PROCESSED, load_config

logger = logging.getLogger(__name__)


def load_master() -> pd.DataFrame:
    path = DATA_PROCESSED / "master_timeseries.csv"
    if not path.exists():
        raise FileNotFoundError("Missing master_timeseries.csv. Run build_features.py first.")
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def before_after_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compare key indicators across baseline/conflict/de-escalation periods."""
    metrics = [
        "DCOILWTICO",
        "DCOILBRENTEU",
        "GASREGW",
        "brent_wti_spread",
        "VIXCLS",
        "SP500",
        "gdelt_news_attention",
    ]
    available = [m for m in metrics if m in df.columns]
    summary = (
        df.groupby("period")[available]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .round(4)
    )
    out = DATA_PROCESSED / "before_after_summary.csv"
    summary.to_csv(out)
    return summary


def lag_correlation(df: pd.DataFrame, max_lag: int = 21) -> pd.DataFrame:
    """Measure how oil price changes lead/lag gasoline price changes."""
    if "DCOILWTICO_change" not in df or "GASREGW_change" not in df:
        raise ValueError("Required change columns missing.")

    rows = []
    for lag in range(0, max_lag + 1):
        shifted_oil = df["DCOILWTICO_change"].shift(lag)
        corr = shifted_oil.corr(df["GASREGW_change"])
        rows.append({"lag_days_oil_leads_gas": lag, "correlation": corr})
    result = pd.DataFrame(rows)
    result.to_csv(DATA_PROCESSED / "lag_correlation_oil_gas.csv", index=False)
    return result


def news_oil_regression(df: pd.DataFrame) -> pd.DataFrame:
    """Regression: oil returns vs media attention and market controls.

    This is not a causal proof. It is an association model showing whether news attention
    and market stress help explain short-term oil moves.
    """
    model_cols = ["DCOILWTICO_return", "gdelt_news_attention", "VIXCLS_change", "SP500_return"]
    available = [c for c in model_cols if c in df.columns]
    data = df[available].replace([np.inf, -np.inf], np.nan).dropna()
    if len(data) < 30 or "DCOILWTICO_return" not in data:
        logger.warning("Not enough rows for news-oil regression.")
        return pd.DataFrame()

    y = data["DCOILWTICO_return"]
    x_cols = [c for c in available if c != "DCOILWTICO_return"]
    X = sm.add_constant(data[x_cols])
    model = sm.OLS(y, X).fit(cov_type="HC3")

    result = pd.DataFrame({
        "term": model.params.index,
        "coefficient": model.params.values,
        "std_error": model.bse.values,
        "p_value": model.pvalues.values,
        "r_squared": model.rsquared,
        "n_obs": int(model.nobs),
    })
    result.to_csv(DATA_PROCESSED / "news_oil_regression.csv", index=False)
    return result


def gasoline_prediction_model(df: pd.DataFrame) -> pd.DataFrame:
    """Simple predictive model for U.S. gasoline prices using oil and market variables."""
    candidate_features = [
        "DCOILWTICO",
        "DCOILBRENTEU",
        "brent_wti_spread",
        "VIXCLS",
        "DFF",
        "gdelt_news_attention",
    ]
    features = [c for c in candidate_features if c in df.columns]
    data = df[["GASREGW", *features]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(data) < 50:
        logger.warning("Not enough rows for gas price model.")
        return pd.DataFrame()

    X = data[features]
    y = data["GASREGW"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)
    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    metrics = {
        "model": "LinearRegression",
        "target": "GASREGW",
        "features": ", ".join(features),
        "mae": mean_absolute_error(y_test, preds),
        "r2": r2_score(y_test, preds),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
    }
    coef = pd.DataFrame({"feature": features, "coefficient": model.coef_})
    coef["intercept"] = model.intercept_
    for k, v in metrics.items():
        coef[k] = v
    coef.to_csv(DATA_PROCESSED / "gasoline_prediction_model.csv", index=False)

    pred_df = pd.DataFrame({"actual_gas_price": y_test.values, "predicted_gas_price": preds}, index=y_test.index)
    pred_df.to_csv(DATA_PROCESSED / "gasoline_prediction_predictions.csv", index=False)
    return coef


def run_all_analyses(config: Dict | None = None) -> Dict[str, pd.DataFrame]:
    config = config or load_config()
    df = load_master()
    max_lag = int(config["analysis"].get("lag_days", 21))
    outputs = {
        "before_after_summary": before_after_summary(df),
        "lag_correlation": lag_correlation(df, max_lag=max_lag),
        "news_oil_regression": news_oil_regression(df),
        "gasoline_prediction_model": gasoline_prediction_model(df),
    }
    return outputs


if __name__ == "__main__":
    from utils import ensure_directories, setup_logging

    setup_logging()
    ensure_directories()
    run_all_analyses()
