# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 6
# Runnable: False
# Hash: d92234f8

objective_weights = {
    'ise': 0.5,         # 50% - primary objective
    'chattering': 0.3,  # 30% - important for smoothness
    'effort': 0.2,      # 20% - energy consideration
}

# Reference values (baseline Classical SMC with manual tuning)
reference_values = {
    'ise': 25.0,
    'chattering': 150.0,
    'effort': 200.0,
}