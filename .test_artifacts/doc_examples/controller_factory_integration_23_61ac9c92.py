# Example from: docs\technical\controller_factory_integration.md
# Index: 23
# Runnable: False
# Hash: 61ac9c92

# example-metadata:
# runnable: false

def compute_gain_sensitivity_matrix(controller_type, nominal_gains, test_states):
    """Compute sensitivity of control performance to gain variations."""

    n_gains = len(nominal_gains)
    n_states = len(test_states)
    sensitivity_matrix = np.zeros((n_states, n_gains))

    delta = 0.01  # 1% perturbation

    for i, state in enumerate(test_states):
        for j, gain in enumerate(nominal_gains):
            # Perturb gain
            perturbed_gains = nominal_gains.copy()
            perturbed_gains[j] *= (1 + delta)

            # Create controllers
            nominal_controller = create_controller(controller_type, gains=nominal_gains)
            perturbed_controller = create_controller(controller_type, gains=perturbed_gains)

            # Compute control actions
            u_nominal = nominal_controller.compute_control(state, (), {}).u
            u_perturbed = perturbed_controller.compute_control(state, (), {}).u

            # Compute sensitivity
            sensitivity_matrix[i, j] = (u_perturbed - u_nominal) / (delta * gain)

    return sensitivity_matrix