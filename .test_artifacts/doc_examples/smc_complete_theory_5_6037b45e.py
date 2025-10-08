# Example from: docs\mathematical_foundations\smc_complete_theory.md
# Index: 5
# Runnable: True
# Hash: 6037b45e

if state_norm > 10.0 or velocity_norm > 50.0:
       # System diverging - reset controller state
       u_int = 0.0
       K = K_init