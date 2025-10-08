# Example from: docs\technical\configuration_schema_reference.md
# Index: 5
# Runnable: True
# Hash: dbc6e214

performance_config = ClassicalSMCConfig(
    gains=[15.0, 12.0, 8.0, 6.0, 25.0, 4.0],  # Aggressive gains
    max_force=150.0,
    boundary_layer=0.01,  # Narrow boundary layer for precision
    dt=0.001,  # High frequency control
    switch_method="linear"
)