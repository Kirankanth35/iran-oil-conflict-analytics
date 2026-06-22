"""Create interactive maps for strategic oil risk locations."""
from __future__ import annotations

import pandas as pd
import folium

from utils import DATA_RAW, MAPS


def build_hormuz_risk_map() -> None:
    locations = pd.read_csv(DATA_RAW / "strategic_locations.csv")
    center = [26.5667, 56.2500]
    m = folium.Map(location=center, zoom_start=4, tiles="CartoDB positron")

    color_map = {
        "Oil chokepoint": "red",
        "Iran capital": "darkred",
        "U.S. capital": "blue",
        "WTI benchmark hub": "green",
        "Energy hub": "green",
        "Financial market hub": "purple",
        "Consumer/fuel market hub": "orange",
        "Energy region": "cadetblue",
    }

    for _, row in locations.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"<b>{row['name']}</b><br>{row['category']}<br>{row['description']}",
            tooltip=row["name"],
            icon=folium.Icon(color=color_map.get(row["category"], "gray")),
        ).add_to(m)

    # Approximate Hormuz transit corridor as a polyline.
    corridor = [
        [26.30, 55.30],
        [26.45, 56.00],
        [26.55, 56.50],
        [25.80, 57.20],
    ]
    folium.PolyLine(
        corridor,
        color="red",
        weight=4,
        opacity=0.7,
        tooltip="Approximate Strait of Hormuz transit corridor",
    ).add_to(m)

    title_html = """
    <h3 style='position: fixed; z-index:9999; top: 10px; left: 50px; background: white; padding: 8px; border: 1px solid #aaa;'>
    U.S.-Iran Oil Risk Map: Chokepoints, Benchmarks, and Business Hubs
    </h3>
    """
    m.get_root().html.add_child(folium.Element(title_html))
    out_path = MAPS / "hormuz_oil_risk_map.html"
    m.save(out_path)


if __name__ == "__main__":
    build_hormuz_risk_map()
