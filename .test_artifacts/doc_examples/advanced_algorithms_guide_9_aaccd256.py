# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 9
# Runnable: True
# Hash: aaccd256

from src.utils.numerical_stability import safe_exp

# Exponential barrier function
def barrier_cost(distance, sharpness=10.0):
    # UNSAFE: exp(1000) overflows
    # return np.exp(-sharpness * distance)

    # SAFE: clipped to prevent overflow
    return safe_exp(-sharpness * distance, max_value=700.0)