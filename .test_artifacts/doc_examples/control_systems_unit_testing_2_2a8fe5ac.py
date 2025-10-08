# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 2
# Runnable: False
# Hash: 2a8fe5ac

def test_gain_positivity_enforcement():
    """Test strict positivity requirements for SMC gains."""
    boundary_layer = 0.1
    max_force = 20.0

    # Test k1 must be strictly positive
    with pytest.raises(ValueError, match="k1.*must be > 0"):
        ClassicalSMC(
            gains=[0.0, 44.45, 17.31, 14.25, 18.66, 9.76],
            max_force=max_force,
            boundary_layer=boundary_layer
        )

    # Test k2 must be strictly positive
    with pytest.raises(ValueError, match="k2.*must be > 0"):
        ClassicalSMC(
            gains=[77.62, -5.0, 17.31, 14.25, 18.66, 9.76],
            max_force=max_force,
            boundary_layer=boundary_layer
        )

    # Test lam1, lam2 must be strictly positive
    with pytest.raises(ValueError, match="lam1.*must be > 0"):
        ClassicalSMC(
            gains=[77.62, 44.45, 0.0, 14.25, 18.66, 9.76],
            max_force=max_force,
            boundary_layer=boundary_layer
        )

    # Test K (switching gain) must be strictly positive
    with pytest.raises(ValueError, match="K.*must be > 0"):
        ClassicalSMC(
            gains=[77.62, 44.45, 17.31, 14.25, -1.0, 9.76],
            max_force=max_force,
            boundary_layer=boundary_layer
        )

    # Test kd (derivative gain) can be zero but not negative
    # This should NOT raise an error
    controller = ClassicalSMC(
        gains=[77.62, 44.45, 17.31, 14.25, 18.66, 0.0],
        max_force=max_force,
        boundary_layer=boundary_layer
    )
    assert controller.kd == 0.0

    # But negative kd should fail
    with pytest.raises(ValueError, match="kd.*must be"):
        ClassicalSMC(
            gains=[77.62, 44.45, 17.31, 14.25, 18.66, -1.0],
            max_force=max_force,
            boundary_layer=boundary_layer
        )