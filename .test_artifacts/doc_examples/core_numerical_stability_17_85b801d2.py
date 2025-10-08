# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 17
# Runnable: False
# Hash: 85b801d2

# Conservative (research-grade precision)
conservative_reg = AdaptiveRegularizer(
    regularization_alpha=1e-6,  # Minimal regularization
    max_condition_number=1e15   # High tolerance
)

# Aggressive (real-time systems)
aggressive_reg = AdaptiveRegularizer(
    regularization_alpha=1e-3,  # Strong regularization
    max_condition_number=1e10   # Low tolerance
)

# Fixed (maximum performance)
fixed_reg = AdaptiveRegularizer(
    use_fixed_regularization=True,
    min_regularization=1e-7
)

# Compare
M_conservative = conservative_reg.regularize_matrix(M)
M_aggressive = aggressive_reg.regularize_matrix(M)
M_fixed = fixed_reg.regularize_matrix(M)

print(f"Conservative κ: {np.linalg.cond(M_conservative):.2e}")
print(f"Aggressive κ: {np.linalg.cond(M_aggressive):.2e}")
print(f"Fixed κ: {np.linalg.cond(M_fixed):.2e}")