# Example from: docs\api\simulation_engine_api_reference.md
# Index: 15
# Runnable: True
# Hash: 71347201

try:
       x_next = dynamics.step(x, u, dt)
   except Exception:
       # Truncate and return