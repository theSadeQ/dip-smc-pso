# Example from: docs\theory\numerical_stability_methods.md
# Index: 12
# Runnable: True
# Hash: f9cf9e17

from src.plant.core.numerical_stability import fast_condition_estimate
kappa = fast_condition_estimate(M)
print(f"Condition number: {kappa:.2e}")