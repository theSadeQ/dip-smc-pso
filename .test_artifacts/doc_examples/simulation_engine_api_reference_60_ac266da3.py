# Example from: docs\api\simulation_engine_api_reference.md
# Index: 60
# Runnable: True
# Hash: ac266da3

u_held = u_n  # Control held constant
x_{n+1} = x_n + dt * f(x_n, u_held, t_n)  # Euler step with held control