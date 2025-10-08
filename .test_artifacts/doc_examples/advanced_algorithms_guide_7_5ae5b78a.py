# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 7
# Runnable: True
# Hash: 5ae5b78a

from src.utils.numerical_stability import safe_divide

# Control law with division
error = state[0]
velocity = state[1]

# UNSAFE: division by zero if velocity = 0
# control = error / velocity

# SAFE: protected division
control = safe_divide(
    error,
    velocity,
    epsilon=1e-12,    # Minimum safe denominator
    fallback=0.0,     # Value if velocity exactly zero
    warn=True         # Issue warning for debugging
)