# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 23
# Runnable: False
# Hash: 0bcc12a5

config = ClassicalSMCConfig(
    gains=[5.0, 3.0, 4.0, 2.0, 10.0, 1.0],  # All positive
    max_force=100.0,                          # Positive force limit
    dt=0.01,                                  # 100 Hz control rate
    boundary_layer=0.01,                      # 1% boundary layer
    boundary_layer_slope=0.1,                 # Mild adaptation
    switch_method="tanh",                     # Smooth switching
    regularization=1e-10,                     # Standard regularization
    controllability_threshold=0.5,            # Moderate threshold
    dynamics_model=None                       # No equivalent control
)