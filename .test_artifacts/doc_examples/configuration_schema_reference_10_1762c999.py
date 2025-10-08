# Example from: docs\technical\configuration_schema_reference.md
# Index: 10
# Runnable: False
# Hash: 1762c999

fast_adaptive_config = AdaptiveSMCConfig(
    gains=[20.0, 15.0, 10.0, 8.0, 5.0],  # Aggressive adaptation rate
    max_force=150.0,
    dt=0.001,
    leak_rate=0.001,        # Minimal leakage
    dead_zone=0.02,         # Narrow dead zone
    adapt_rate_limit=20.0,  # Fast adaptation
    K_min=0.1,
    K_max=200.0,
    boundary_layer=0.01
)