# Example from: docs\technical\factory_usage_examples.md
# Index: 6
# Runnable: True
# Hash: a905480f

from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

# Configuration for robust adaptation
adaptive_config = AdaptiveSMCConfig(
    gains=[15.0, 12.0, 8.0, 6.0, 3.0],  # [k1, k2, λ1, λ2, γ]
    max_force=150.0,
    leak_rate=0.01,         # Parameter drift prevention
    dead_zone=0.05,         # Adaptation dead zone
    adapt_rate_limit=10.0,  # Maximum adaptation rate
    K_min=0.1,              # Minimum adaptive gain
    K_max=100.0,            # Maximum adaptive gain
    gamma=2.0,              # Adaptation rate
    boundary_layer=0.1,     # Smooth switching layer
    smooth_switch=True,     # Enable smooth switching
    dt=0.001
)

controller = create_controller('adaptive_smc', config=adaptive_config)

# Access adaptation bounds
bounds = adaptive_config.get_adaptation_bounds()
print(f"Adaptation bounds: {bounds}")