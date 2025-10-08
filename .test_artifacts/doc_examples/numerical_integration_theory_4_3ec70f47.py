# Example from: docs\mathematical_foundations\numerical_integration_theory.md
# Index: 4
# Runnable: False
# Hash: 3ec70f47

# example-metadata:
# runnable: false

# PSO optimization (speed critical)
simulation_config_pso = {
    'method': 'euler',
    'dt': 0.005,
    'duration': 5.0,
}

# Development/debugging
simulation_config_dev = {
    'method': 'rk4',
    'dt': 0.01,
    'duration': 10.0,
}

# Production deployment
simulation_config_prod = {
    'method': 'rk45',
    'rtol': 1e-6,
    'atol': 1e-9,
    'duration': 10.0,
    'max_step': 0.1,  # Prevent huge steps
}