# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 6
# Runnable: False
# Hash: bf9c25d8

# example-metadata:
# runnable: false

def fitness_function(gains_array):
    """PSO fitness evaluation for hybrid controller.

    The hybrid controller's complexity requires careful fitness design:
    - Control effort weighted heavily (prevents aggressive adaptation)
    - Tracking error with time-varying weights
    - Stability margins included in cost
    """
    controller = create_hybrid_controller(gains_array)

    # Multi-objective fitness components
    tracking_error = compute_tracking_metrics(controller)
    control_effort = compute_control_energy(controller)
    stability_margin = compute_stability_measures(controller)

    return w1*tracking_error + w2*control_effort + w3*stability_margin