# Example from: docs\validation\simulation_result_validation.md
# Index: 17
# Runnable: True
# Hash: ac567687

from src.analysis.validation.statistical_tests import StatisticalTestSuite

suite = StatisticalTestSuite()
result = suite.validate(data, test_types=['normality_tests'])

shapiro = result.data['normality_tests']['shapiro_wilk']
print(f"W = {shapiro['statistic']:.4f}, p = {shapiro['p_value']:.4f}")