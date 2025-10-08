# Example from: docs\validation\simulation_result_validation.md
# Index: 32
# Runnable: True
# Hash: c1dcccb4

weights = {'settling_time': 0.3, 'overshoot': 0.5, 'control_effort': 0.2}

# Compute weighted scores
for method_name, method_data in performance_data.items():
    score = sum(weights[m] * normalize(method_data[m]) for m in weights)