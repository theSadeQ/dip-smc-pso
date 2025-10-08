# Example from: docs\PSO_INTEGRATION_GUIDE.md
# Index: 2
# Runnable: True
# Hash: d99b2c21

from src.controllers.factory import get_gain_bounds_for_pso, validate_smc_gains

# Get optimization bounds
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
lower_bounds, upper_bounds = bounds

# Example PSO fitness function
def fitness_function(gains):
    """PSO fitness function for controller tuning."""
    # Validate gains first
    if not validate_smc_gains(SMCType.CLASSICAL, gains):
        return 1e6  # High penalty for invalid gains

    try:
        # Create controller
        controller = create_smc_for_pso(SMCType.CLASSICAL, gains, plant_config)

        # Evaluate performance across test scenarios
        total_cost = 0.0
        test_states = [
            np.array([0.1, 0.2, 0.3, 0.0, 0.0, 0.0]),
            np.array([0.2, 0.1, 0.4, 0.1, 0.0, 0.0]),
        ]

        for state in test_states:
            control = controller.compute_control(state)

            # Cost function: state error + control effort
            state_cost = np.sum(state[:3]**2)
            control_cost = np.sum(control**2)
            total_cost += state_cost + 0.1 * control_cost

        return total_cost

    except Exception:
        return 1e6  # High penalty for errors

# Use with PySwarms or other PSO libraries
# bounds = (lower_bounds, upper_bounds)
# optimizer.optimize(fitness_function, bounds=bounds)