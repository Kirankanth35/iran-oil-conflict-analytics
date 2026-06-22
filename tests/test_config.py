from pathlib import Path
import yaml


def test_config_loads():
    path = Path(__file__).resolve().parents[1] / "config" / "config.yaml"
    config = yaml.safe_load(path.read_text())
    assert "fred" in config
    assert "event_windows" in config
    assert "DCOILWTICO" in config["fred"]["series"]
