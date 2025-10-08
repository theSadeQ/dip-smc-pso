# Example from: docs\factory\factory_api_reference.md
# Index: 10
# Runnable: True
# Hash: 6c693b55

controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001
)