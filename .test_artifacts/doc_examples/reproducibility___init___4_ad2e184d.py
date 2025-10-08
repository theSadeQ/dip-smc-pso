# Example from: docs\reference\utils\reproducibility___init__.md
# Index: 4
# Runnable: True
# Hash: ad2e184d

from src.utils.reproducibility import capture_random_state, restore_random_state
import numpy as np

# Generate some random numbers
set_seed(42)
values_before = np.random.randn(5)

# Capture current RNG state
state = capture_random_state()

# Generate more numbers (changes state)
np.random.randn(100)

# Restore previous state
restore_random_state(state)

# Continue from captured state
values_after = np.random.randn(5)

# Should match continuation from before
print("State restoration allows sequence continuation")