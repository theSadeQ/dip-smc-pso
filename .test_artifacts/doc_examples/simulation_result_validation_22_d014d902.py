# Example from: docs\validation\simulation_result_validation.md
# Index: 22
# Runnable: True
# Hash: d014d902

result = suite.validate(data, test_types=['power_analysis'])
power_analysis = result.data['power_analysis']

print(f"Current power: {power_analysis['estimated_power']:.2f}")
print(f"Recommended N: {power_analysis['recommended_sample_size']}")

if not power_analysis['power_adequate']:
    print("⚠ Insufficient power - need more data")