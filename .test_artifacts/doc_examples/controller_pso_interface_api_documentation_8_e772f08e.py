# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 8
# Runnable: False
# Hash: e772f08e

# Adaptive SMC Gains: [c1, λ1, c2, λ2, γ] ∈ ℝ⁵
ADAPTIVE_SMC_GAINS = {
    'c1': 'Sliding surface gain for θ₁',
    'lambda1': 'Sliding surface coefficient for θ₁',
    'c2': 'Sliding surface gain for θ₂',
    'lambda2': 'Sliding surface coefficient for θ₂',
    'gamma': 'Adaptation rate'
}

ADAPTIVE_SMC_BOUNDS = {
    'lower': [0.1, 0.1, 0.1, 0.1, 0.01],
    'upper': [20.0, 20.0, 20.0, 20.0, 5.0]
}