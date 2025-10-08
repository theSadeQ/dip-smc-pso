# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 10
# Runnable: False
# Hash: 75ece5a1

# Stability-focused configuration
stability_config = ClassicalSMCConfig(
    gains=[5.0, 5.0, 3.0, 3.0, 10.0, 1.0],  # Conservative gains
    max_force=100.0,
    boundary_layer=0.05,  # Wider boundary layer
    switch_method="tanh"
)

# Performance-focused configuration
performance_config = ClassicalSMCConfig(
    gains=[15.0, 12.0, 8.0, 6.0, 25.0, 4.0],  # Aggressive gains
    max_force=150.0,
    boundary_layer=0.01,  # Narrow boundary layer
    switch_method="linear"
)

# Research configuration with custom parameters
research_config = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001,  # High-frequency control
    boundary_layer_slope=1.0,  # Adaptive boundary
    regularization=1e-8,
    controllability_threshold=0.1
)