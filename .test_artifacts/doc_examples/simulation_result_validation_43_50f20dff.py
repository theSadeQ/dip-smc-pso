# Example from: docs\validation\simulation_result_validation.md
# Index: 43
# Runnable: True
# Hash: 50f20dff

# Check normality first
normality = suite.validate(data, test_types=['normality_tests'])

if normality_rejected:
    # Use non-parametric test
    use_mann_whitney_u()  # Instead of t-test
    # OR transform data
    log_data = np.log(data)
    # OR use bootstrap CI