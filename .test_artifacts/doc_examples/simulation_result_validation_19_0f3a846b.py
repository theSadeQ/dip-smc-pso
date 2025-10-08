# Example from: docs\validation\simulation_result_validation.md
# Index: 19
# Runnable: True
# Hash: 0f3a846b

result = suite.validate(data, test_types=['hypothesis_tests'])
ttest = result.data['hypothesis_tests']['one_sample']['t_test_zero_mean']

if ttest['p_value'] < 0.05:
    print(f"Mean significantly different from 0 (p={ttest['p_value']:.4f})")