# Example from: docs\technical\factory_usage_examples.md
# Index: 1
# Runnable: True
# Hash: b3983f1e

from src.controllers.factory import create_controller

# Classical SMC with minimal configuration
classical_controller = create_controller(
    controller_type='classical_smc',
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0]
)

# Super-Twisting SMC with optimized gains (Issue #2 resolution)
sta_controller = create_controller(
    controller_type='sta_smc',
    gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43]  # Reduced overshoot configuration
)

# Adaptive SMC with standard gains
adaptive_controller = create_controller(
    controller_type='adaptive_smc',
    gains=[12.0, 10.0, 6.0, 5.0, 2.5]
)

# Hybrid controller with surface gains only
hybrid_controller = create_controller(
    controller_type='hybrid_adaptive_sta_smc',
    gains=[8.0, 6.0, 4.0, 3.0]
)