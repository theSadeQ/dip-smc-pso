# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 21
# Runnable: True
# Hash: b45f8d77

# Increase regularization
matrix_regularization = 1e-8  # In equivalent control

# Reduce adaptation rate limits
adapt_rate_limit = 2.0  # From default 5.0

# Check system conditioning
condition_number = np.linalg.cond(inertia_matrix)
if condition_number > 1e12:
    print("WARNING: Ill-conditioned system")