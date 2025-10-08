# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 6
# Runnable: True
# Hash: e3e55c87

def test_lyapunov_decrease_ratio_monitoring():
    """Test LDR monitoring for stability assessment."""
    from src.utils.monitoring.stability import LyapunovDecreaseMonitor

    dt = 0.01
    monitor = LyapunovDecreaseMonitor(
        window_size_ms=300.0,
        dt=dt,
        ldr_threshold=0.95,
        transient_time=1.0
    )

    controller = create_test_controller()

    # Simulate trajectory
    state = np.array([0.1, 0.2, -0.1, 0.0, 0.3, -0.2])
    history = {}

    ldr_values = []

    for step in range(200):  # 2 seconds simulation
        result = controller.compute_control(state, (), history)

        # Extract sliding surface and update monitor
        sigma = np.array([history['sigma'][-1]])
        monitor_result = monitor.update(sigma)

        # After transient period, check LDR
        if monitor_result['status'] != 'transient':
            ldr = monitor_result['ldr']
            ldr_values.append(ldr)

            # LDR should be high (>95%) for stable control
            if len(ldr_values) > 50:  # After enough samples
                recent_ldr = np.mean(ldr_values[-50:])
                assert recent_ldr >= 0.90, \
                    f"LDR too low: {recent_ldr:.2%} (should be ≥90%)"

        # Simple state update (mock dynamics)
        state[3:] += -0.1 * state[:3] * dt  # Simplified dynamics
        state[:3] += state[3:] * dt