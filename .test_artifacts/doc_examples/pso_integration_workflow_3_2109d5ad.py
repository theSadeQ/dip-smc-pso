# Example from: docs\factory\pso_integration_workflow.md
# Index: 3
# Runnable: True
# Hash: 2109d5ad

def setup_adaptive_smc_pso_optimization(
    plant_config: Any,
    adaptation_focused: bool = True
) -> Dict[str, Any]:
    """
    Setup PSO optimization for Adaptive SMC with adaptation-focused tuning.

    Adaptive SMC Parameters: [k1, k2, λ1, λ2, γ]
    - k1, k2: Pendulum surface gains
    - λ1, λ2: Sliding coefficients
    - γ: Adaptation rate (critical parameter)
    """

    # Adaptation-focused bounds
    if adaptation_focused:
        bounds = {
            'lower': [8.0, 8.0, 5.0, 5.0, 1.0],     # Higher surface gains
            'upper': [60.0, 50.0, 40.0, 35.0, 8.0]  # Conservative adaptation rate
        }
    else:
        bounds = {
            'lower': [5.0, 5.0, 3.0, 3.0, 0.5],
            'upper': [50.0, 40.0, 30.0, 25.0, 10.0]
        }

    # PSO configuration with emphasis on exploration for adaptation
    pso_config = {
        'swarm_size': 40,           # Larger swarm for adaptation exploration
        'max_iterations': 150,      # More iterations for convergence
        'cognitive_param': 2.5,     # Higher personal exploration
        'social_param': 1.5,        # Lower social influence
        'inertia_weight': 0.9,
        'inertia_decay': 0.98,      # Slower decay for exploration
        'adaptation_penalty_weight': 0.2,  # Penalty for poor adaptation
        'convergence_threshold': 5e-7
    }

    # Create PSO interface
    pso_interface = PSOFactoryInterface('adaptive_smc', plant_config)
    controller_factory = pso_interface.create_pso_controller_factory()

    def adaptive_fitness_function(gains: GainsArray) -> float:
        """Fitness function emphasizing adaptation performance."""

        try:
            controller = controller_factory(gains)

            # Extract adaptation rate for analysis
            gamma = gains[4]

            # Adaptive-specific test scenarios
            scenarios = [
                ('adaptation_test_1', np.array([0.2, 0.3, 0.1, 0.0, 0.0, 0.0])),
                ('adaptation_test_2', np.array([0.4, 0.5, 0.3, 0.5, 0.3, 0.2])),
                ('parameter_change', np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0]))  # For adaptation testing
            ]

            total_cost = 0.0

            for i, (scenario_name, initial_state) in enumerate(scenarios):
                if scenario_name == 'parameter_change':
                    # Test adaptation to parameter changes
                    cost = evaluate_adaptation_performance(controller, initial_state)
                else:
                    # Standard performance evaluation
                    cost = evaluate_scenario_performance(controller, initial_state, simulation_time=3.0)

                total_cost += cost

            # Adaptation rate penalty
            if gamma < 0.5 or gamma > 8.0:
                total_cost += 50.0 * abs(gamma - 3.0)  # Penalty for extreme adaptation rates

            # Convergence bonus for reasonable adaptation rates
            if 1.0 <= gamma <= 5.0:
                total_cost *= 0.9  # 10% bonus for good adaptation rate

            return total_cost

        except Exception as e:
            logger.warning(f"Adaptive fitness evaluation failed: {e}")
            return 1500.0

    return {
        'controller_factory': controller_factory,
        'fitness_function': adaptive_fitness_function,
        'bounds': bounds,
        'pso_config': pso_config,
        'pso_interface': pso_interface,
        'n_gains': 5,
        'optimization_type': 'adaptive_smc_dip',
        'special_features': ['adaptation_monitoring', 'parameter_change_testing']
    }

def evaluate_adaptation_performance(
    controller: PSOControllerWrapper,
    initial_state: StateVector,
    simulation_time: float = 4.0
) -> float:
    """Evaluate adaptation performance with parameter changes."""

    from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics

    dynamics = SimplifiedDIPDynamics()
    dt = 0.001
    n_steps = int(simulation_time / dt)
    state = initial_state.copy()

    adaptation_errors = []
    pre_change_errors = []
    post_change_errors = []
    change_step = n_steps // 2  # Parameter change at midpoint

    for step in range(n_steps):
        try:
            # Simulate parameter change at midpoint
            if step == change_step:
                # Introduce disturbance to test adaptation
                state += np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0])

            control = controller.compute_control(state)
            result = dynamics.compute_dynamics(state, control)

            if not result.success:
                break

            state = state + dt * result.state_derivative
            position_error = np.linalg.norm(state[:3])

            if step < change_step:
                pre_change_errors.append(position_error)
            else:
                post_change_errors.append(position_error)

            adaptation_errors.append(position_error)

            if np.any(np.abs(state) > 8.0):
                return 2000.0  # Adaptation failure penalty

        except Exception:
            return 2000.0

    # Analyze adaptation performance
    pre_change_avg = np.mean(pre_change_errors) if pre_change_errors else 1.0
    post_change_avg = np.mean(post_change_errors) if post_change_errors else 1.0

    # Adaptation quality metric
    adaptation_ratio = post_change_avg / (pre_change_avg + 1e-6)

    # Cost emphasizing good adaptation
    adaptation_cost = (
        5.0 * np.mean(adaptation_errors) +      # Overall performance
        10.0 * max(0, adaptation_ratio - 2.0) + # Penalty for poor adaptation
        2.0 * post_change_avg                   # Post-change performance
    )

    return adaptation_cost