# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 10
# Runnable: False
# Hash: 280430a5

# example-metadata:
# runnable: false

# Hybrid Adaptive STA-SMC Gains: [c1, λ1, c2, λ2] ∈ ℝ⁴
HYBRID_ADAPTIVE_STA_SMC_GAINS = {
    'c1': 'Proportional-like sliding surface gain',
    'lambda1': 'Integral-like sliding surface coefficient',
    'c2': 'Proportional-like sliding surface gain',
    'lambda2': 'Integral-like sliding surface coefficient'
}

HYBRID_ADAPTIVE_STA_SMC_BOUNDS = {
    'lower': [0.1, 0.1, 0.1, 0.1],
    'upper': [20.0, 20.0, 20.0, 20.0]
}