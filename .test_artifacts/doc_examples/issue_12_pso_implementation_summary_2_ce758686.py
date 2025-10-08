# Example from: docs\issue_12_pso_implementation_summary.md
# Index: 2
# Runnable: False
# Hash: ce758686

# example-metadata:
# runnable: false

def simulate_and_evaluate(gains, controller_type, config, dynamics):
    """Direct simulation with explicit chattering metrics."""

    # No excessive normalization
    control_derivative = np.gradient(control_hist, dt)
    time_domain_index = np.sqrt(np.mean(control_derivative**2))

    # FFT spectral analysis
    spectrum = np.abs(fft(control_hist))
    hf_power_ratio = high_freq_power / total_power  # f > 10 Hz

    # Combined chattering index (Issue #12 metric)
    chattering_index = 0.7 * time_domain_index + 0.3 * hf_power_ratio

    # Multi-objective fitness with explicit penalties
    chattering_penalty = max(0.0, chattering_index - 2.0) * 10.0
    tracking_penalty = max(0.0, tracking_error_rms - 0.1) * 100.0
    effort_penalty = max(0.0, control_effort_rms - 100.0) * 0.1

    fitness = tracking_error_rms + chattering_penalty + tracking_penalty + effort_penalty
    return fitness