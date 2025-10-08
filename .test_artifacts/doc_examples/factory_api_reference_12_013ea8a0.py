# Example from: docs\factory\factory_api_reference.md
# Index: 12
# Runnable: True
# Hash: 013ea8a0

controller = create_controller(
    'sta_smc',
    gains=[25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
    max_force=150.0,
    dt=0.001,
    power_exponent=0.5,
    regularization=1e-6,
    switch_method='tanh'
)