# Example from: docs\validation\simulation_result_validation.md
# Index: 39
# Runnable: True
# Hash: 1e25430e

# Always check power
result = suite.validate(data, test_types=['power_analysis'])
if not result.data['power_analysis']['power_adequate']:
    print(f"⚠ Need {result.data['power_analysis']['recommended_sample_size']} samples")