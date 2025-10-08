# Example from: docs\validation\simulation_result_validation.md
# Index: 20
# Runnable: True
# Hash: a76b5d62

config = StatisticalTestConfig(
    use_paired_tests=True,  # Use paired if same scenarios
    significance_level=0.05
)
suite = StatisticalTestSuite(config)