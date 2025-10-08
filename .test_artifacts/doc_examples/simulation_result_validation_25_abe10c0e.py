# Example from: docs\validation\simulation_result_validation.md
# Index: 25
# Runnable: True
# Hash: abe10c0e

benchmark = BenchmarkSuite(config)

result = benchmark.validate(
    data=None,
    methods=[controller_A, controller_B, controller_C],
    simulation_function=run_simulation,
    test_cases=[scenario1, scenario2, scenario3]
)

sig_tests = result.data['statistical_significance_testing']
ranking = result.data['ranking_analysis']['final_ranking']