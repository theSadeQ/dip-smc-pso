# Example from: docs\api\simulation_engine_api_reference.md
# Index: 58
# Runnable: True
# Hash: 2b47a67b

dp45 = IntegratorFactory.create_integrator(
    'dormand_prince',
    dt=0.01,           # Initial step size
    atol=1e-6,         # Absolute error tolerance
    rtol=1e-3,         # Relative error tolerance
    min_step=1e-6,     # Minimum allowed step size
    max_step=0.1,      # Maximum allowed step size
    safety_factor=0.9  # Step size adjustment factor
)