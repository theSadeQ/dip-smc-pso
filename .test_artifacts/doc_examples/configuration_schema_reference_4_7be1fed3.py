# Example from: docs\technical\configuration_schema_reference.md
# Index: 4
# Runnable: True
# Hash: 7be1fed3

stability_config = ClassicalSMCConfig(
    gains=[5.0, 5.0, 3.0, 3.0, 10.0, 1.0],  # Conservative gains
    max_force=100.0,
    boundary_layer=0.05,  # Wide boundary layer for robustness
    dt=0.01,
    switch_method="tanh"
)