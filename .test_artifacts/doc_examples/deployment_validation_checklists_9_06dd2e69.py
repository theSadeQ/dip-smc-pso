# Example from: docs\deployment_validation_checklists.md
# Index: 9
# Runnable: False
# Hash: 06dd2e69

def run_load_testing():
    """Execute comprehensive load testing."""
    load_scenarios = [
        {'name': 'normal_load', 'multiplier': 1.0, 'duration': 3600},
        {'name': 'high_load', 'multiplier': 1.5, 'duration': 1800},
        {'name': 'peak_load', 'multiplier': 2.0, 'duration': 900},
        {'name': 'stress_load', 'multiplier': 3.0, 'duration': 300}
    ]

    results = {}
    for scenario in load_scenarios:
        result = execute_load_scenario(scenario)
        results[scenario['name']] = result

        # Validate performance under load
        assert result.success_rate > 0.95
        assert result.average_response_time < 20  # ms
        assert result.memory_usage < 800  # MB

    return results