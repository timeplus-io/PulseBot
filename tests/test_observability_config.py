from pulsebot.config import Config, ObservabilityConfig


def test_default_observability_config():
    cfg = Config()
    assert cfg.observability.events.enabled is True
    assert cfg.observability.events.min_severity == "info"


def test_observability_config_from_dict():
    cfg = Config(**{
        "observability": {
            "events": {
                "enabled": False,
                "min_severity": "warning",
            }
        }
    })
    assert cfg.observability.events.enabled is False
    assert cfg.observability.events.min_severity == "warning"
