# Example from: docs\deployment_validation_checklists.md
# Index: 14
# Runnable: False
# Hash: f86849a3

def establish_performance_baselines():
    """Establish performance baselines for monitoring."""
    baseline_tests = [
        ('control_loop_frequency', measure_control_frequency),
        ('response_time', measure_response_time),
        ('memory_usage', measure_memory_usage),
        ('cpu_utilization', measure_cpu_utilization),
        ('optimization_time', measure_optimization_time)
    ]

    baselines = {}
    for metric_name, measurement_func in baseline_tests:
        baseline_value = measurement_func()
        baselines[metric_name] = {
            'value': baseline_value,
            'timestamp': datetime.now().isoformat(),
            'measurement_duration': 300  # 5 minutes
        }

    # Store baselines for future comparison
    save_performance_baselines(baselines)
    return baselines