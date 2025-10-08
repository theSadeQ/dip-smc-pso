# Example from: docs\factory\pso_integration_workflow.md
# Index: 4
# Runnable: True
# Hash: 99ad56a8

def setup_super_twisting_smc_pso_optimization(
    plant_config: Any,
    high_performance_mode: bool = True
) -> Dict[str, Any]:
    """
    Setup PSO optimization for Super-Twisting SMC.

    STA-SMC Parameters: [K1, K2, k1, k2, λ1, λ2]
    - K1, K2: Super-twisting algorithm gains (K1 > K2 typically)
    - k1, k2: Surface gains
    - λ1, λ2: Sliding coefficients
    """

    # High-performance bounds for aggressive STA tuning
    if high_performance_mode:
        bounds = {
            'lower': [15.0, 10.0, 8.0, 8.0, 5.0, 5.0],
            'upper': [100.0, 70.0, 60.0, 50.0, 40.0, 35.0]
        }
    else:
        bounds = {
            'lower': [10.0, 8.0, 5.0, 5.0, 3.0, 3.0],
            'upper': [80.0, 60.0, 50.0, 40.0, 30.0, 25.0]
        }

    # STA-specific PSO configuration
    pso_config = {
        'swarm_size': 35,
        'max_iterations': 120,
        'cognitive_param': 2.2,
        'social_param': 1.8,
        'inertia_weight': 0.85,
        'inertia_decay': 0.97,
        'sta_constraint_weight': 0.3,  # Weight for STA-specific constraints
        'convergence_threshold': 1e-6
    }

    pso_interface = PSOFactoryInterface('sta_smc', plant_config)
    controller_factory = pso_interface.create_pso_controller_factory()

    def sta_fitness_function(gains: GainsArray) -> float:
        """Fitness function for Super-Twisting SMC optimization."""

        try:
            controller = controller_factory(gains)

            K1, K2 = gains[0], gains[1]

            # STA constraint penalty
            sta_penalty = 0.0
            if K1 <= K2:
                sta_penalty += 100.0 * (K2 - K1 + 1.0)  # Strong penalty for K1 <= K2

            # Test with challenging scenarios for STA performance
            scenarios = [
                ('precision_tracking', np.array([0.05, 0.03, 0.02, 0.0, 0.0, 0.0])),
                ('large_disturbance', np.array([0.6, 0.8, 0.4, 0.3, 0.2, 0.1])),
                ('high_frequency', np.array([0.2, 0.2, 0.2, 2.0, 1.5, 1.0]))
            ]

            total_cost = 0.0
            scenario_weights = [0.4, 0.4, 0.2]

            for weight, (scenario_name, initial_state) in zip(scenario_weights, scenarios):
                if scenario_name == 'precision_tracking':
                    # STA excels at precision - test with tighter tolerance
                    cost = evaluate_sta_precision_performance(controller, initial_state)
                elif scenario_name == 'large_disturbance':
                    # Test robustness with large disturbances
                    cost = evaluate_sta_robustness_performance(controller, initial_state)
                else:
                    # Standard evaluation
                    cost = evaluate_scenario_performance(controller, initial_state)

                total_cost += weight * cost

            total_cost += sta_penalty

            # Bonus for optimal K1/K2 ratio
            k_ratio = K1 / K2
            if 1.2 <= k_ratio <= 2.0:  # Optimal STA ratio range
                total_cost *= 0.95  # 5% bonus

            return total_cost

        except Exception as e:
            logger.warning(f"STA fitness evaluation failed: {e}")
            return 1800.0

    return {
        'controller_factory': controller_factory,
        'fitness_function': sta_fitness_function,
        'bounds': bounds,
        'pso_config': pso_config,
        'pso_interface': pso_interface,
        'n_gains': 6,
        'optimization_type': 'sta_smc_dip',
        'special_features': ['finite_time_convergence', 'chattering_reduction', 'robustness_testing']
    }

def evaluate_sta_precision_performance(
    controller: PSOControllerWrapper,
    initial_state: StateVector,
    precision_threshold: float = 0.01
) -> float:
    """Evaluate STA precision performance with tight tolerances."""

    from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics

    dynamics = SimplifiedDIPDynamics()
    dt = 0.001
    simulation_time = 3.0
    n_steps = int(simulation_time / dt)
    state = initial_state.copy()

    precision_errors = []
    convergence_time = None

    for step in range(n_steps):
        try:
            control = controller.compute_control(state)
            result = dynamics.compute_dynamics(state, control)

            if not result.success:
                break

            state = state + dt * result.state_derivative
            position_error = np.linalg.norm(state[:3])
            precision_errors.append(position_error)

            # Check for convergence to precision threshold
            if convergence_time is None and position_error < precision_threshold:
                convergence_time = step * dt

            if np.any(np.abs(state) > 5.0):
                return 1500.0  # Precision failure

        except Exception:
            return 1500.0

    # Precision-focused cost function
    avg_precision_error = np.mean(precision_errors)
    final_precision_error = precision_errors[-1]

    # Convergence time bonus
    convergence_bonus = 0.0
    if convergence_time is not None:
        convergence_bonus = max(0, 2.0 - convergence_time)  # Bonus for fast convergence

    precision_cost = (
        20.0 * avg_precision_error +
        30.0 * final_precision_error -
        5.0 * convergence_bonus
    )

    return max(0.1, precision_cost)  # Minimum positive cost

def evaluate_sta_robustness_performance(
    controller: PSOControllerWrapper,
    initial_state: StateVector
) -> float:
    """Evaluate STA robustness with large disturbances."""

    from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics

    dynamics = SimplifiedDIPDynamics()
    dt = 0.001
    simulation_time = 4.0
    n_steps = int(simulation_time / dt)
    state = initial_state.copy()

    robustness_errors = []
    max_recovery_time = 0.0
    disturbance_steps = [n_steps // 4, n_steps // 2, 3 * n_steps // 4]

    for step in range(n_steps):
        try:
            # Apply disturbances at specific intervals
            if step in disturbance_steps:
                disturbance = np.array([0.1, 0.1, 0.05, 0.2, 0.1, 0.1])
                state += disturbance

            control = controller.compute_control(state)
            result = dynamics.compute_dynamics(state, control)

            if not result.success:
                break

            state = state + dt * result.state_derivative
            position_error = np.linalg.norm(state[:3])
            robustness_errors.append(position_error)

            if np.any(np.abs(state) > 8.0):
                return 2000.0  # Robustness failure

        except Exception:
            return 2000.0

    # Robustness cost emphasizing disturbance rejection
    avg_robustness_error = np.mean(robustness_errors)
    max_error = np.max(robustness_errors)

    robustness_cost = (
        15.0 * avg_robustness_error +
        10.0 * max_error +
        5.0 * robustness_errors[-1]  # Final steady-state error
    )

    return robustness_cost