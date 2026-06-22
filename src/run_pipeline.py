"""One-command pipeline runner."""
from __future__ import annotations

import logging

from utils import ensure_directories, load_config, setup_logging
from fetch_fred import fetch_all_fred
from fetch_gdelt import fetch_gdelt_timeline
from build_features import build_master_table
from analysis import run_all_analyses
from visualize import create_all_charts
from maps import build_hormuz_risk_map
from business_impact_model import build_business_risk_index

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    ensure_directories()
    config = load_config()

    fetch_all_fred(config)
    if config.get("gdelt", {}).get("enabled", True):
        try:
            fetch_gdelt_timeline(config)
        except Exception as exc:  # noqa: BLE001
            logger.warning("GDELT fetch failed; continuing without news attention: %s", exc)

    build_master_table(config)
    run_all_analyses(config)
    build_business_risk_index()
    create_all_charts(config)
    build_hormuz_risk_map()
    logger.info("Pipeline complete. Check reports/figures and reports/maps.")


if __name__ == "__main__":
    main()
