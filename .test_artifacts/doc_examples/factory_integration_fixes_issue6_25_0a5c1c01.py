# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 25
# Runnable: False
# Hash: 0a5c1c01

# example-metadata:
# runnable: false

# Ensure all surface gains are positive
config = ClassicalSMCConfig(
    gains=[1.0, 5.0, 3.0, 2.0, 10.0, 1.0],  # k1 > 0
    max_force=150.0,
    boundary_layer=0.02
)

# Check gain constraints:
# - Position gains k1, k2 > 0
# - Surface coefficients λ1, λ2 > 0
# - Switching gain K > 0
# - Derivative gain kd ≥ 0