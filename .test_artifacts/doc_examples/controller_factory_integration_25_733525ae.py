# Example from: docs\technical\controller_factory_integration.md
# Index: 25
# Runnable: False
# Hash: 733525ae

def compare_controller_performance(controller_types, test_scenarios):
    """Statistically compare performance of different controller types."""

    results = {}

    for controller_type in controller_types:
        controller = create_controller(controller_type)

        # Collect performance metrics
        settling_times = []
        overshoots = []
        steady_state_errors = []

        for scenario in test_scenarios:
            metrics = simulate_control_scenario(controller, scenario)
            settling_times.append(metrics['settling_time'])
            overshoots.append(metrics['overshoot'])
            steady_state_errors.append(metrics['steady_state_error'])

        results[controller_type] = {
            'settling_time': {
                'mean': np.mean(settling_times),
                'std': np.std(settling_times),
                'confidence_interval': compute_confidence_interval(settling_times)
            },
            'overshoot': {
                'mean': np.mean(overshoots),
                'std': np.std(overshoots),
                'confidence_interval': compute_confidence_interval(overshoots)
            },
            'steady_state_error': {
                'mean': np.mean(steady_state_errors),
                'std': np.std(steady_state_errors),
                'confidence_interval': compute_confidence_interval(steady_state_errors)
            }
        }

    return results