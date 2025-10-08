# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 10
# Runnable: False
# Hash: 4bfbdf36

def compute_control_performance_metrics(simulation_result: Dict[str, Any],
                                      objectives: List[str]) -> float:
    """
    Compute multi-objective performance metrics for PSO optimization.

    Available Objectives:
    - 'ise': Integral of Squared Error
    - 'itae': Integral of Time-weighted Absolute Error
    - 'overshoot': Maximum overshoot percentage
    - 'settling_time': 2% settling time
    - 'control_effort': RMS control effort
    - 'chattering_index': Chattering severity measure

    Mathematical Definitions:

    ISE: ∫₀ᵀ ||e(t)||² dt
    where e(t) = x_desired(t) - x(t)

    ITAE: ∫₀ᵀ t||e(t)|| dt
    Emphasizes later-time errors

    Overshoot: max(|x(t) - x_final|/x_final) × 100%

    Settling Time: min{t : |x(τ) - x_final| ≤ 0.02|x_final| ∀τ ≥ t}

    Control Effort: √(1/T ∫₀ᵀ u²(t) dt)

    Chattering Index: ∫₀ᵀ |du/dt| dt
    Measures control signal smoothness
    """

    t = simulation_result['time']
    x = simulation_result['state']
    u = simulation_result['control']

    # Extract individual metrics
    metrics = {}

    if 'ise' in objectives:
        error = x - np.zeros_like(x)  # Assuming regulation to origin
        metrics['ise'] = np.trapz(np.sum(error**2, axis=1), t)

    if 'itae' in objectives:
        error = np.abs(x - np.zeros_like(x))
        time_weighted_error = t.reshape(-1, 1) * np.sum(error, axis=1).reshape(-1, 1)
        metrics['itae'] = np.trapz(time_weighted_error.flatten(), t)

    if 'overshoot' in objectives:
        # Compute maximum overshoot for each state
        final_values = x[-1, :]
        max_deviation = np.max(np.abs(x - final_values), axis=0)
        overshoot = np.max(max_deviation / (np.abs(final_values) + 1e-8)) * 100
        metrics['overshoot'] = overshoot

    if 'settling_time' in objectives:
        # 2% settling time calculation
        final_values = x[-1, :]
        tolerance = 0.02 * (np.abs(final_values) + 1e-8)

        settling_times = []
        for i, state in enumerate(x.T):
            within_tolerance = np.abs(state - final_values[i]) <= tolerance[i]
            # Find last time outside tolerance
            if np.any(~within_tolerance):
                last_violation = np.where(~within_tolerance)[0][-1]
                settling_times.append(t[last_violation])
            else:
                settling_times.append(0.0)

        metrics['settling_time'] = max(settling_times)

    if 'control_effort' in objectives:
        metrics['control_effort'] = np.sqrt(np.mean(u**2))

    if 'chattering_index' in objectives:
        du_dt = np.gradient(u, t)
        metrics['chattering_index'] = np.trapz(np.abs(du_dt), t)

    # Combine metrics using weighted sum (default equal weights)
    weights = {
        'ise': 0.25,
        'itae': 0.15,
        'overshoot': 0.2,
        'settling_time': 0.15,
        'control_effort': 0.15,
        'chattering_index': 0.1
    }

    # Normalize metrics to [0, 1] range for fair weighting
    normalized_metrics = {}
    for metric_name, value in metrics.items():
        if metric_name in ['ise', 'itae']:
            # Lower is better, normalize by expected range
            normalized_metrics[metric_name] = min(value / 100.0, 1.0)
        elif metric_name == 'overshoot':
            # Overshoot penalty (0-50% range)
            normalized_metrics[metric_name] = min(value / 50.0, 1.0)
        elif metric_name == 'settling_time':
            # Settling time penalty (0-10s range)
            normalized_metrics[metric_name] = min(value / 10.0, 1.0)
        elif metric_name in ['control_effort', 'chattering_index']:
            # Control effort penalty
            normalized_metrics[metric_name] = min(value / 150.0, 1.0)

    # Compute weighted fitness score
    fitness = sum(weights.get(name, 0) * value
                  for name, value in normalized_metrics.items())

    return fitness