# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 10
# Runnable: True
# Hash: 55f3088b

from src.utils.numerical_stability import safe_normalize

# Normalized gradient for optimization
gradient = compute_gradient(params)

# UNSAFE: if gradient is exactly zero
# step_direction = gradient / np.linalg.norm(gradient)

# SAFE: returns zero vector if gradient is zero
step_direction = safe_normalize(
    gradient,
    min_norm=1e-15,
    fallback=np.zeros_like(gradient)
)