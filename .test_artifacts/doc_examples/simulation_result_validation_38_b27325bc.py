# Example from: docs\validation\simulation_result_validation.md
# Index: 38
# Runnable: False
# Hash: b27325bc

config = BenchmarkConfig(
    measure_computation_time=True,
    n_trials=100
)

benchmark = BenchmarkSuite(config)
result = benchmark.validate(...)

comp_time = result.data['simulation_benchmarks'][scenario][method]['computational_analysis']

mean_time = comp_time['mean_computation_time']
std_time = comp_time['std_computation_time']
worst_case_time = comp_time['mean_computation_time'] + 3*comp_time['std_computation_time']

if worst_case_time < control_period:
    print("✓ Real-time feasible")
else:
    print("✗ Timing constraint violated")