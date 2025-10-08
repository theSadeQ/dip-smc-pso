# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 8
# Runnable: False
# Hash: 76a96874

# example-metadata:
# runnable: false

def test_chattering_reduction_with_large_boundary_layer():
    """Test that large boundary layer (9.76) effectively reduces chattering."""
    optimal_gains = [77.62, 44.45, 17.31, 14.25, 18.66, 9.76]

    # Test with optimal boundary layer
    controller_optimal = ClassicalSMC(
        gains=optimal_gains,
        max_force=20.0,
        boundary_layer=9.76,  # Large boundary layer
        switch_method='tanh'
    )

    # Test with small boundary layer for comparison
    controller_small_bl = ClassicalSMC(
        gains=optimal_gains,
        max_force=20.0,
        boundary_layer=0.1,  # Small boundary layer
        switch_method='tanh'
    )

    # Simulate near sliding surface
    state = np.array([0.0, 0.01, 0.01, 0.0, 0.05, 0.05])

    controls_optimal = []
    controls_small_bl = []

    for _ in range(100):
        result_optimal = controller_optimal.compute_control(state, (), {})
        result_small_bl = controller_small_bl.compute_control(state, (), {})

        controls_optimal.append(result_optimal.u)
        controls_small_bl.append(result_small_bl.u)

    # Measure control signal variation (chattering indicator)
    control_variation_optimal = np.std(np.diff(controls_optimal))
    control_variation_small = np.std(np.diff(controls_small_bl))

    # Large boundary layer should reduce variation significantly
    assert control_variation_optimal < 0.5 * control_variation_small, \
        f"Large boundary layer should reduce chattering: " \
        f"optimal={control_variation_optimal:.4f}, " \
        f"small={control_variation_small:.4f}"