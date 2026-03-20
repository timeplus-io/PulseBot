from pulsebot.config import Config, ObservabilityConfig


def test_default_observability_config():
    cfg = Config()
    assert cfg.observability.events.enabled is True
    assert cfg.observability.events.min_severity == "info"
    assert cfg.observability.events.heartbeat_interval == 60
    assert cfg.observability.events.include_debug_state is False


def test_observability_config_from_dict():
    cfg = Config(**{
        "observability": {
            "events": {
                "enabled": False,
                "min_severity": "warning",
                "heartbeat_interval": 0,
                "include_debug_state": True,
            }
        }
    })
    assert cfg.observability.events.enabled is False
    assert cfg.observability.events.min_severity == "warning"
    assert cfg.observability.events.heartbeat_interval == 0
    assert cfg.observability.events.include_debug_state is True
