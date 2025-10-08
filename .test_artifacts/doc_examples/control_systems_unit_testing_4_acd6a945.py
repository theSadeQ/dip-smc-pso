# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 4
# Runnable: False
# Hash: acd6a945

# example-metadata:
# runnable: false

def test_physical_state_bounds():
    """Test controller behavior within and beyond physical limits."""
    controller = create_test_controller()

    # Test states within normal operating range
    normal_states = [
        np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Equilibrium
        np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0]),  # Small displacement
        np.array([0.5, 0.3, 0.2, 0.0, 0.0, 0.0]),  # Moderate displacement
    ]

    for state in normal_states:
        result = controller.compute_control(state, (), {})

        # Control must be finite and bounded
        assert np.isfinite(result.u)
        assert abs(result.u) <= controller.max_force

    # Test extreme but valid states
    extreme_states = [
        np.array([0.0, np.pi/6, np.pi/6, 0.0, 2.0, 2.0]),  # Large angles/velocities
        np.array([1.0, -np.pi/4, np.pi/4, 0.5, -1.5, 1.0]),  # Mixed extremes
    ]

    for state in extreme_states:
        result = controller.compute_control(state, (), {})

        # Must still produce finite, bounded control
        assert np.isfinite(result.u)
        assert abs(result.u) <= controller.max_force