# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 24
# Runnable: False
# Hash: c23608fb

# example-metadata:
# runnable: false

# Zero gain - should raise ValueError
invalid_config = ClassicalSMCConfig(
    gains=[0.0, 3.0, 4.0, 2.0, 10.0, 1.0],  # k1 = 0!
    max_force=100.0,
    dt=0.01,
    boundary_layer=0.01
)

# Negative switching gain - should raise ValueError
invalid_config = ClassicalSMCConfig(
    gains=[5.0, 3.0, 4.0, 2.0, -10.0, 1.0],  # K < 0!
    max_force=100.0,
    dt=0.01,
    boundary_layer=0.01
)

# Zero boundary layer - should raise ValueError
invalid_config = ClassicalSMCConfig(
    gains=[5.0, 3.0, 4.0, 2.0, 10.0, 1.0],
    max_force=100.0,
    dt=0.01,
    boundary_layer=0.0  # ε = 0!
)