# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 4
# Runnable: False
# Hash: e4fe5566

# Classical SMC Gains: [c1, λ1, c2, λ2, K, kd] ∈ ℝ⁶
CLASSICAL_SMC_GAINS = {
    'c1': 'Sliding surface gain for θ₁ error',
    'lambda1': 'Sliding surface coefficient for θ₁',
    'c2': 'Sliding surface gain for θ₂ error',
    'lambda2': 'Sliding surface coefficient for θ₂',
    'K': 'Control gain',
    'kd': 'Derivative gain'
}

# Typical bounds for PSO optimization:
CLASSICAL_SMC_BOUNDS = {
    'lower': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    'upper': [20.0, 20.0, 20.0, 20.0, 100.0, 10.0]
}