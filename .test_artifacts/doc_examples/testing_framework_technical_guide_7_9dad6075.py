# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 7
# Runnable: True
# Hash: 9dad6075

# tests/conftest.py
import pytest
import numpy as np
from pathlib import Path
from types import SimpleNamespace

@pytest.fixture(scope="session")
def config():
    """Load configuration from config.yaml for tests.

    Provides session-scoped configuration to avoid repeated file I/O.
    Backfills controller_defaults gains for core controllers.
    """
    import yaml

    raw = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8")) or {}

    def _to_ns(obj):
        """Convert dict to SimpleNamespace for attribute access."""
        if isinstance(obj, dict):
            return SimpleNamespace(**{k: _to_ns(v) for k, v in obj.items()})
        return obj

    cfg = _to_ns(raw)

    # Backfill controller_defaults if missing
    if not hasattr(cfg, "controller_defaults"):
        cfg.controller_defaults = SimpleNamespace()

    # Ensure all core controllers have default gains
    defaults = {
        "classical_smc": [10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
        "adaptive_smc": [10.0, 8.0, 15.0, 12.0, 0.5],
        "sta_smc": [25.0, 10.0, 15.0, 12.0, 20.0, 15.0],
        "hybrid_adaptive_sta_smc": [15.0, 12.0, 18.0, 15.0]
    }

    for ctrl_name, default_gains in defaults.items():
        if not hasattr(cfg.controller_defaults, ctrl_name):
            setattr(cfg.controller_defaults, ctrl_name, SimpleNamespace(gains=default_gains))

    return cfg

@pytest.fixture(scope="session")
def physics_cfg(config):
    """Physics parameters from configuration."""
    return config.physics

@pytest.fixture(scope="session")
def dynamics_simplified(physics_cfg):
    """Session-scoped simplified dynamics model."""
    from src.core.dynamics import SimplifiedDynamics
    return SimplifiedDynamics(physics_cfg)

@pytest.fixture(scope="session")
def dynamics_full(physics_cfg):
    """Session-scoped full nonlinear dynamics model."""
    from src.core.dynamics_full import FullNonlinearDynamics
    return FullNonlinearDynamics(physics_cfg)