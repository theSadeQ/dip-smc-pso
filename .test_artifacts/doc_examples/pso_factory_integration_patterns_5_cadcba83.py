# Example from: docs\pso_factory_integration_patterns.md
# Index: 5
# Runnable: False
# Hash: cadcba83

def constrained_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Advanced PSO with stability constraints and adaptive bounds."""

    # Get base bounds
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(controller_type)

    # Create constraint functions based on control theory
    def stability_constraint(gains: np.ndarray) -> bool:
        """Verify closed-loop stability constraints."""

        if controller_type == SMCType.CLASSICAL:
            k1, k2, lam1, lam2, K, kd = gains

            # Sliding surface stability (Hurwitz condition)
            if lam1 <= 0 or lam2 <= 0:
                return False

            # Reaching condition constraint
            if K <= 0:
                return False

            # Practical stability margins
            if lam1/k1 > 20 or lam2/k2 > 20:  # Avoid overly aggressive surfaces
                return False

            # Chattering prevention
            if K > 100:  # Excessive switching gain
                return False

        elif controller_type == SMCType.ADAPTIVE:
            k1, k2, lam1, lam2, gamma = gains

            # Adaptation rate constraints
            if gamma <= 0 or gamma > 20:
                return False

            # Surface stability
            if lam1 <= 0 or lam2 <= 0:
                return False

        return True

    # Create factory with constraint checking
    base_factory = create_pso_controller_factory(controller_type)

    def constrained_factory(gains: np.ndarray):
        """Factory with built-in constraint checking."""

        # Check stability constraints
        if not stability_constraint(gains):
            raise ValueError("Stability constraints violated")

        return base_factory(gains)

    # Enhanced fitness function
    def constrained_fitness_function(gains: np.ndarray) -> float:
        """Fitness function with constraint penalties."""

        try:
            # Check basic validity
            if not validate_smc_gains(controller_type, gains):
                return 1e6

            # Check stability constraints
            if not stability_constraint(gains):
                return 1e6

            # Create and evaluate controller
            controller = constrained_factory(gains)
            metrics = evaluate_controller_performance(controller)

            # Multi-objective fitness with penalties
            base_fitness = (
                0.4 * metrics['ise'] +                    # Control performance
                0.3 * metrics['settling_time'] +          # Speed
                0.2 * metrics['control_effort'] +         # Efficiency
                0.1 * metrics['overshoot']                # Stability margin
            )

            # Add constraint penalties
            penalty = 0.0

            # Chattering penalty
            if 'chattering_index' in metrics and metrics['chattering_index'] > 0.1:
                penalty += 100 * metrics['chattering_index']

            # Control saturation penalty
            if 'saturation_ratio' in metrics and metrics['saturation_ratio'] > 0.05:
                penalty += 50 * metrics['saturation_ratio']

            return base_fitness + penalty

        except Exception as e:
            return 1e6  # Severe penalty for failed evaluations

    # Adaptive PSO configuration
    adaptive_config = {
        'n_particles': 50,
        'max_iter': 150,
        'bounds': (lower_bounds, upper_bounds),
        'w': 0.9,
        'c1': 2.0,
        'c2': 2.0,
        'early_stopping': True,
        'patience': 20,
        'min_improvement': 1e-6
    }

    # Run constrained optimization
    tuner = PSOTuner(
        controller_factory=constrained_fitness_function,
        config=config,
        **adaptive_config
    )

    return tuner.optimize()