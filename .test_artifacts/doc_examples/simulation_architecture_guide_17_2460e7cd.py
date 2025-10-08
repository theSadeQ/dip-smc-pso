# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 17
# Runnable: True
# Hash: 2460e7cd

# GOOD: Creates view (zero-copy)
x_array = np.asarray(x, dtype=float)  # If x is already float64 ndarray

# BAD: Creates copy
x_array = np.array(x, dtype=float)  # Always creates new array