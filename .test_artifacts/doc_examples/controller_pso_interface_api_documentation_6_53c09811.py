# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 6
# Runnable: False
# Hash: 53c09811

# example-metadata:
# runnable: false

# STA-SMC Gains: [K1, K2, k1, k2, λ1, λ2] ∈ ℝ⁶
STA_SMC_GAINS = {
    'K1': 'First-order sliding mode gain',
    'K2': 'Second-order sliding mode gain',
    'k1': 'Surface gain for θ₁',
    'k2': 'Surface gain for θ₂',
    'lambda1': 'Surface coefficient for θ₁',
    'lambda2': 'Surface coefficient for θ₂'
}

# Optimized bounds from Issue #2 resolution:
STA_SMC_BOUNDS = {
    'lower': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    'upper': [20.0, 20.0, 20.0, 20.0, 10.0, 10.0]
}