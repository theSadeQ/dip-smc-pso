# Example from: docs\configuration_integration_documentation.md
# Index: 2
# Runnable: True
# Hash: 3c28cae2

# Highest priority - always used when provided
controller = create_controller(
    'classical_smc',
    gains=[20, 15, 12, 8, 35, 5],    # Explicit gains
    max_force=150.0,                  # Explicit max_force
    boundary_layer=0.02               # Explicit boundary_layer
)