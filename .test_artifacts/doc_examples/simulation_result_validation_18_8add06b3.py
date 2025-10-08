# Example from: docs\validation\simulation_result_validation.md
# Index: 18
# Runnable: True
# Hash: 8add06b3

result = suite.validate(data, test_types=['stationarity_tests'])
adf = result.data['stationarity_tests']['augmented_dickey_fuller']

print(f"ADF statistic: {adf['test_statistic']:.4f}")
print(f"Conclusion: {adf['conclusion']}")