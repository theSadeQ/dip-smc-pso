# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 15
# Runnable: False
# Hash: 03dd6655

# example-metadata:
# runnable: false

def fitness_function(gains_array):
    """PSO fitness evaluation for classical SMC."""
    # Create controller with candidate gains
    controller = ClassicalSMC(
        gains=gains_array,
        max_force=100.0,
        boundary_layer=0.01
    )

    # Run simulation
    result = run_simulation(controller, duration=5.0, dt=0.01)

    # Compute multi-objective fitness
    tracking_error = compute_ise(result.states)
    control_effort = compute_rms(result.controls)
    chattering = compute_chattering_index(result.controls)

    # Weighted cost
    return (0.5 * tracking_error +
            0.3 * control_effort +
            0.2 * chattering)