# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 8
# Runnable: False
# Hash: fc2caf7c

# example-metadata:
# runnable: false

# Tighten parameter bounds
custom_bounds = {
    'lower': [1.0, 1.0, 1.0, 1.0, 5.0, 0.5],   # More conservative
    'upper': [10.0, 10.0, 10.0, 10.0, 50.0, 5.0]  # Reduced ranges
}

# Increase stability weight in cost function
stability_focused_weights = {
    'state_error': 1.0,
    'control_effort': 0.01,
    'control_rate': 0.001,
    'stability': 50.0  # Heavily penalize instability
}