"""Create publication-quality charts for the project."""
from __future__ import annotations

import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import FIGURES, DATA_PROCESSED, load_config

logger = logging.getLogger(__name__)


def load_master() -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED / "master_timeseries.csv", parse_dates=["date"])


def _add_event_lines(ax, config):
    conflict_start = pd.to_datetime(config["event_windows"]["conflict_start"])
    deesc_start = pd.to_datetime(config["event_windows"]["tentative_deescalation_start"])
    ax.axvline(conflict_start, linestyle="--", linewidth=1, label="Conflict start")
    ax.axvline(deesc_start, linestyle=":", linewidth=1, label="De-escalation / deal window")


def oil_price_event_chart(df: pd.DataFrame, config) -> None:
    cols = [c for c in ["DCOILWTICO", "DCOILBRENTEU"] if c in df.columns]
    fig, ax = plt.subplots(figsize=(12, 6))
    for col in cols:
        ax.plot(df["date"], df[col], label=col)
    _add_event_lines(ax, config)
    ax.set_title("Oil Prices Around U.S.-Iran Conflict Risk Window")
    ax.set_xlabel("Date")
    ax.set_ylabel("USD per barrel")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES / "01_oil_prices_event_window.png", dpi=200)
    plt.close(fig)


def gasoline_pass_through_chart(df: pd.DataFrame, config) -> None:
    fig, ax1 = plt.subplots(figsize=(12, 6))
    if "DCOILWTICO" in df:
        ax1.plot(df["date"], df["DCOILWTICO"], label="WTI crude", alpha=0.85)
    ax1.set_ylabel("WTI crude, USD/barrel")
    ax2 = ax1.twinx()
    if "GASREGW" in df:
        ax2.plot(df["date"], df["GASREGW"], label="U.S. gasoline", alpha=0.85)
    ax2.set_ylabel("Gasoline, USD/gallon")
    _add_event_lines(ax1, config)
    ax1.set_title("Oil-to-Gasoline Pass-Through")
    ax1.set_xlabel("Date")
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="best")
    ax1.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES / "02_oil_to_gasoline_pass_through.png", dpi=200)
    plt.close(fig)


def news_attention_chart(df: pd.DataFrame, config) -> None:
    if "gdelt_news_attention" not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["date"], df["gdelt_news_attention"], label="GDELT news attention")
    _add_event_lines(ax, config)
    ax.set_title("Global Media Attention: Iran / Hormuz / Oil Risk")
    ax.set_xlabel("Date")
    ax.set_ylabel("Share of global online news matching query")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES / "03_gdelt_news_attention.png", dpi=200)
    plt.close(fig)


def before_after_boxplot(df: pd.DataFrame) -> None:
    metric = "DCOILWTICO"
    if metric not in df.columns:
        return
    periods = ["pre_conflict", "conflict", "deescalation"]
    data = [df.loc[df["period"] == p, metric].dropna() for p in periods]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(data, tick_labels=periods, showmeans=True)
    ax.set_title("Before / During / After Comparison: WTI Oil Price")
    ax.set_ylabel("USD per barrel")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES / "04_before_after_wti_boxplot.png", dpi=200)
    plt.close(fig)


def lag_correlation_chart() -> None:
    path = DATA_PROCESSED / "lag_correlation_oil_gas.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["lag_days_oil_leads_gas"], df["correlation"], marker="o")
    ax.set_title("Lag Correlation: WTI Changes Leading Gasoline Changes")
    ax.set_xlabel("Lag days: oil leads gasoline")
    ax.set_ylabel("Correlation")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES / "05_lag_correlation_oil_gas.png", dpi=200)
    plt.close(fig)


def correlation_matrix(df: pd.DataFrame) -> None:
    cols = [
        "DCOILWTICO_return",
        "DCOILBRENTEU_return",
        "GASREGW_change",
        "VIXCLS_change",
        "SP500_return",
        "gdelt_news_attention",
    ]
    cols = [c for c in cols if c in df.columns]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right")
    ax.set_yticklabels(cols)
    ax.set_title("Correlation Matrix: Oil, Gasoline, Markets, News")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(FIGURES / "06_correlation_matrix.png", dpi=200)
    plt.close(fig)


def create_all_charts(config=None):
    config = config or load_config()
    df = load_master()
    oil_price_event_chart(df, config)
    gasoline_pass_through_chart(df, config)
    news_attention_chart(df, config)
    before_after_boxplot(df)
    lag_correlation_chart()
    correlation_matrix(df)
    logger.info("Charts saved in %s", FIGURES)


if __name__ == "__main__":
    from utils import ensure_directories, setup_logging

    setup_logging()
    ensure_directories()
    create_all_charts()
