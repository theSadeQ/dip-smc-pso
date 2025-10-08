# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 12
# Runnable: True
# Hash: 647369fc

from src.plant.core import fast_condition_estimate

# Compare with exact computation
M = np.random.randn(3, 3)
M = M @ M.T  # Make symmetric positive definite

exact_cond = np.linalg.cond(M)
approx_cond = fast_condition_estimate(M)

print(f"Exact: {exact_cond:.2e}")
print(f"Approximate: {approx_cond:.2e}")
print(f"Relative error: {abs(exact_cond - approx_cond) / exact_cond * 100:.1f}%")