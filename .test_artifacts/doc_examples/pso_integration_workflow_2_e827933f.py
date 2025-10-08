# Example from: docs\factory\pso_integration_workflow.md
# Index: 2
# Runnable: True
# Hash: e827933f

def setup_classical_smc_pso_optimization(
    plant_config: Any,
    optimization_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Setup PSO optimization for Classical SMC with enhanced performance.

    Classical SMC Parameters: [k1, k2, λ1, λ2, K, kd]
    - k1, k2: Pendulum surface gains (convergence rate)
    - λ1, λ2: Sliding coefficients (surface slope)
    - K: Switching gain (uncertainty rejection)
    - kd: Damping gain (chattering reduction)
    """

    # Enhanced bounds for double-inverted pendulum
    bounds = {
        'lower': [5.0, 5.0, 3.0, 3.0, 10.0, 1.0],    # Conservative lower bounds
        'upper': [50.0, 40.0, 30.0, 25.0, 80.0, 15.0] # Aggressive upper bounds
    }

    # PSO-specific configuration
    default_config = {
        'swarm_size': 30,
        'max_iterations': 100,
        'cognitive_param': 2.0,     # Personal best weight
        'social_param': 2.0,        # Global best weight
        'inertia_weight': 0.9,      # Exploration vs exploitation
        'inertia_decay': 0.95,      # Dynamic inertia reduction
        'convergence_threshold': 1e-6,
        'parallel_evaluation': True,
        'thread_count': 4
    }

    if optimization_config:
        default_config.update(optimization_config)

    # Create PSO factory interface
    pso_interface = PSOFactoryInterface('classical_smc', plant_config)
    controller_factory = pso_interface.create_pso_controller_factory()

    # Fitness function for classical SMC
    def fitness_function(gains: GainsArray) -> float:
        """
        Multi-objective fitness function for Classical SMC optimization.

        Objectives:
        1. Stabilization performance (primary)
        2. Control effort minimization (secondary)
        3. Chattering reduction (tertiary)
        """

        try:
            controller = controller_factory(gains)

            # Test scenarios
            scenarios = [
                ('small_disturbance', np.array([0.1, 0.05, 0.03, 0.0, 0.0, 0.0])),
                ('medium_angles', np.array([0.3, 0.4, 0.2, 0.1, 0.0, 0.0])),
                ('high_velocity', np.array([0.1, 0.1, 0.1, 1.5, 1.0, 0.8]))
            ]

            total_cost = 0.0
            scenario_weights = [0.5, 0.3, 0.2]  # Weight different scenarios

            for weight, (scenario_name, initial_state) in zip(scenario_weights, scenarios):
                scenario_cost = evaluate_scenario_performance(
                    controller, initial_state, simulation_time=2.0
                )
                total_cost += weight * scenario_cost

            # Penalize extreme gains
            gain_penalty = compute_gain_penalty(gains, bounds)
            total_cost += 0.1 * gain_penalty

            return total_cost

        except Exception as e:
            logger.warning(f"Fitness evaluation failed: {e}")
            return 1000.0  # High penalty for failed evaluations

    return {
        'controller_factory': controller_factory,
        'fitness_function': fitness_function,
        'bounds': bounds,
        'pso_config': default_config,
        'pso_interface': pso_interface,
        'n_gains': 6,
        'optimization_type': 'classical_smc_dip'
    }

def evaluate_scenario_performance(
    controller: PSOControllerWrapper,
    initial_state: StateVector,
    simulation_time: float = 2.0,
    dt: float = 0.001
) -> float:
    """Evaluate controller performance for a specific scenario."""

    from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics

    # Create dynamics model
    dynamics = SimplifiedDIPDynamics()

    # Simulation parameters
    n_steps = int(simulation_time / dt)
    state = initial_state.copy()

    # Performance metrics
    position_errors = []
    control_efforts = []
    control_variations = []
    previous_control = 0.0

    for step in range(n_steps):
        try:
            # Compute control
            control = controller.compute_control(state)
            control_value = control[0]

            # Store metrics
            position_error = np.linalg.norm(state[:3])  # Position error magnitude
            position_errors.append(position_error)
            control_efforts.append(abs(control_value))

            # Control variation (chattering metric)
            control_variation = abs(control_value - previous_control)
            control_variations.append(control_variation)
            previous_control = control_value

            # Simulate dynamics
            result = dynamics.compute_dynamics(state, control)
            if not result.success:
                break

            # Integrate
            state = state + dt * result.state_derivative

            # Stability check
            if np.any(np.abs(state) > 10.0):
                return 1000.0  # Instability penalty

        except Exception:
            return 1000.0  # Simulation failure penalty

    # Compute composite cost
    avg_position_error = np.mean(position_errors)
    avg_control_effort = np.mean(control_efforts)
    avg_control_variation = np.mean(control_variations)
    final_position_error = position_errors[-1]

    # Multi-objective cost function
    cost = (
        10.0 * avg_position_error +        # Primary: tracking performance
        0.1 * avg_control_effort +         # Secondary: control effort
        1.0 * avg_control_variation +      # Tertiary: chattering
        5.0 * final_position_error         # Final: steady-state error
    )

    return cost

def compute_gain_penalty(gains: GainsArray, bounds: Dict[str, List[float]]) -> float:
    """Compute penalty for gains near boundaries."""

    gains_array = np.asarray(gains)
    lower_bounds = np.array(bounds['lower'])
    upper_bounds = np.array(bounds['upper'])

    # Normalize gains to [0, 1] range
    normalized_gains = (gains_array - lower_bounds) / (upper_bounds - lower_bounds)

    # Penalty for gains too close to boundaries
    boundary_penalty = 0.0
    for g in normalized_gains:
        if g < 0.1 or g > 0.9:  # Within 10% of boundaries
            boundary_penalty += 1.0

    return boundary_penalty