# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 1
# Runnable: False
# Hash: 63fc0c4b

# example-metadata:
# runnable: false

def test_classical_smc_initialization():
    """Test Classical SMC initialization with valid parameters."""
    # Optimal gains from PSO optimization (report.log line 2)
    gains = [77.62, 44.45, 17.31, 14.25, 18.66, 9.76]
    boundary_layer = 9.76  # Matched to kd for chattering reduction
    max_force = 20.0

    controller = ClassicalSMC(
        gains=gains,
        max_force=max_force,
        boundary_layer=boundary_layer,
        switch_method='tanh'
    )

    # Verify gains unpacked correctly
    assert controller.k1 == pytest.approx(77.62, rel=1e-6)
    assert controller.k2 == pytest.approx(44.45, rel=1e-6)
    assert controller.lam1 == pytest.approx(17.31, rel=1e-6)
    assert controller.lam2 == pytest.approx(14.25, rel=1e-6)
    assert controller.K == pytest.approx(18.66, rel=1e-6)
    assert controller.kd == pytest.approx(9.76, rel=1e-6)

    # Verify boundary layer for chattering reduction
    assert controller.epsilon0 == pytest.approx(9.76)

    # Verify control authority limits
    assert controller.max_force == 20.0