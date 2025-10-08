# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 8
# Runnable: True
# Hash: 1ce092a8

from src.utils.numerical_stability import safe_sqrt

# Norm computation from squared values
squared_sum = x**2 + y**2 + z**2

# UNSAFE: if squared_sum slightly negative due to numerical error
# norm = np.sqrt(squared_sum)

# SAFE: clips to non-negative
norm = safe_sqrt(squared_sum, min_value=1e-15)