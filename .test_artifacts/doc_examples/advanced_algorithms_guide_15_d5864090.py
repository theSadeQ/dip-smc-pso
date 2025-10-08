# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 15
# Runnable: True
# Hash: d5864090

from src.utils.numerical_stability import safe_divide, safe_sqrt, safe_exp

# Protect all potentially unstable operations
result = safe_divide(numerator, denominator, epsilon=1e-12)
norm = safe_sqrt(squared_sum, min_value=1e-15)
exponential = safe_exp(large_value, max_value=700.0)