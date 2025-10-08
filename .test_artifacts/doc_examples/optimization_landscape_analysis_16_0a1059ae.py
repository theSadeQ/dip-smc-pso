# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 16
# Runnable: False
# Hash: 0a1059ae

# example-metadata:
# runnable: false

exploration_bounds = {
    'classical_smc': [
        (0.1, 50.0),    # k1 - wide range
        (0.1, 50.0),    # k2
        (0.1, 50.0),    # λ1
        (0.1, 50.0),    # λ2
        (1.0, 200.0),   # K - full range
        (0.0, 50.0),    # kd
    ],
}