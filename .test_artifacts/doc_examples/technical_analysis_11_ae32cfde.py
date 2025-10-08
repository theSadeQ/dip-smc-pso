# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 11
# Runnable: False
# Hash: ae32cfde

# example-metadata:
# runnable: false

performance_metrics = {
    'test_execution_time': {
        'total_duration': '45 minutes 23 seconds',
        'average_per_test': '5.04 seconds',
        'slowest_tests': [
            ('test_batch_pso_optimization', '8m 34s'),
            ('test_memory_stress_test', '6m 12s'),
            ('test_numerical_stability_monte_carlo', '4m 56s')
        ],
        'fastest_tests': [
            ('test_controller_instantiation', '0.12s'),
            ('test_basic_configuration', '0.08s'),
            ('test_simple_math_operations', '0.05s')
        ]
    },
    'memory_consumption': {
        'peak_usage': '2.1 GB',
        'baseline_usage': '45.2 MB',
        'memory_efficiency': 0.67,  # 67% efficient usage
        'gc_collections': 847,
        'large_object_allocations': 23
    },
    'cpu_utilization': {
        'average_cpu': '78%',
        'peak_cpu': '95%',
        'cpu_efficiency': 0.82,
        'parallel_test_efficiency': 0.71  # 71% parallel efficiency
    }
}