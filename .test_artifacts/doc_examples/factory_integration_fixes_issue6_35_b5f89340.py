# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 35
# Runnable: False
# Hash: b5f89340

# example-metadata:
# runnable: false

# The factory has robust import fallbacks:
# 1. src.core.dynamics.DIPDynamics (preferred)
# 2. src.core.dynamics.DIPDynamics (alternative)
# 3. src.plant.models.simplified.dynamics.SimplifiedDIPDynamics (fallback)

# Ensure at least one dynamics implementation is available
from src.core.dynamics import DIPDynamics
from src.config import load_config

config = load_config("config.yaml")
dynamics = DIPDynamics(config.physics)

# Pass dynamics explicitly if needed
controller = create_controller(
    controller_type='classical_smc',
    config=config,
    gains=[...],
)