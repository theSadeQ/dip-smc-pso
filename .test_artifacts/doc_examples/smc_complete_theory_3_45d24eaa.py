# Example from: docs\mathematical_foundations\smc_complete_theory.md
# Index: 3
# Runnable: True
# Hash: 45d24eaa

controllability = abs(L @ M_inv @ B)
   if controllability < ε_threshold:
       # System near uncontrollable configuration
       u_eq = 0.0  # Disable equivalent control