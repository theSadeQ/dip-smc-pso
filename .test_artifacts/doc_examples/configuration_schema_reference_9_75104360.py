# Example from: docs\technical\configuration_schema_reference.md
# Index: 9
# Runnable: False
# Hash: 75104360

# example-metadata:
# runnable: false

robust_adaptive_config = AdaptiveSMCConfig(
    gains=[15.0, 12.0, 8.0, 6.0, 2.0],  # Conservative adaptation rate
    max_force=150.0,
    dt=0.001,
    leak_rate=0.05,         # Higher leakage for robustness
    dead_zone=0.1,          # Wider dead zone
    adapt_rate_limit=5.0,   # Conservative adaptation
    K_min=1.0,
    K_max=50.0,
    boundary_layer=0.05
)