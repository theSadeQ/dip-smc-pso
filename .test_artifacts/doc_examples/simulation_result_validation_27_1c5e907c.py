# Example from: docs\validation\simulation_result_validation.md
# Index: 27
# Runnable: True
# Hash: 1c5e907c

robustness = result.data['robustness_comparison']

for method_name, metrics in robustness['robustness_metrics'].items():
    cv = metrics['settling_time']['coefficient_of_variation']
    score = metrics['settling_time']['robustness_score']
    print(f"{method_name}: CV={cv:.3f}, Robustness Score={score:.3f}")