# Example from: docs\reference\utils\reproducibility___init__.md
# Index: 1
# Runnable: True
# Hash: d0b194e2

from src.utils.reproducibility import set_seed
import numpy as np

# Set global seed for reproducibility
set_seed(42)

# Generate random numbers
random_values_1 = np.random.randn(10)

# Reset seed - get same sequence
set_seed(42)
random_values_2 = np.random.randn(10)

# Verify reproducibility
assert np.allclose(random_values_1, random_values_2)
print("✓ Reproducibility verified")