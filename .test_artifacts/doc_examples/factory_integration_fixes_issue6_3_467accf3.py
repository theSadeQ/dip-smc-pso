# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 3
# Runnable: True
# Hash: 467accf3

controller = create_controller(
    controller_type='adaptive_smc',
    gains=[12.0, 10.0, 6.0, 5.0, 2.5]
)

# With adaptation parameters
from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

adaptive_config = AdaptiveSMCConfig(
    gains=[12.0, 10.0, 6.0, 5.0, 2.5],
    max_force=150.0,
    leak_rate=0.01,
    dead_zone=0.05,
    adapt_rate_limit=10.0,
    K_min=0.1,
    K_max=100.0,
    gamma=2.0
)

controller = create_controller('adaptive_smc', config=adaptive_config)