# Example from: docs\testing\guides\integration_workflows.md
# Index: 8
# Runnable: True
# Hash: a603c970

@pytest.mark.parametrize("mass_error", [0.8, 0.9, 1.1, 1.2])
def test_robust_integration(mass_error):
    """Integration test with plant uncertainties"""
    perturbed_dynamics = DoublePendulum(
        m1=M1_NOMINAL * mass_error,
        m2=M2_NOMINAL * mass_error
    )

    trajectory = simulate(controller, perturbed_dynamics, [0.2, 0, 0, 0], 5.0)
    assert np.linalg.norm(trajectory[-1]) < 0.1