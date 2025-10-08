# Example from: docs\test_infrastructure_documentation.md
# Index: 6
# Runnable: False
# Hash: b15a15a5

@pytest.mark.numerical_robustness
@pytest.mark.statistical
def test_controller_robustness_monte_carlo():
    """Statistical validation of controller robustness."""
    base_params = get_nominal_physics_params()

    for trial in range(1000):
        # Add ±20% parameter uncertainty
        perturbed_params = add_parameter_uncertainty(base_params, std_dev=0.2)
        dynamics = DIPDynamics(params=perturbed_params)

        controller = ClassicalSMC(gains=optimized_gains)
        performance = evaluate_stabilization(controller, dynamics, sim_time=5.0)

        assert performance.settling_time < 3.0
        assert performance.overshoot < 0.15