# Example from: docs\validation\simulation_result_validation.md
# Index: 26
# Runnable: True
# Hash: c6390c50

for comparison, test in sig_tests['corrected_tests'].items():
    if test['corrected_significant']:
        print(f"{comparison}: Significant difference (p={test['corrected_p_value']:.4f})")
    else:
        print(f"{comparison}: No significant difference")