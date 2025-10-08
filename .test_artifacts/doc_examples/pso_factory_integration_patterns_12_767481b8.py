# Example from: docs\pso_factory_integration_patterns.md
# Index: 12
# Runnable: False
# Hash: 767481b8

# example-metadata:
# runnable: false

def adaptive_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Adaptive PSO with dynamic parameter adjustment."""

    factory = create_pso_controller_factory(controller_type)

    class AdaptivePSOController:
        """Adaptive PSO controller with factory integration."""

        def __init__(self):
            self.iteration = 0
            self.best_fitness_history = []
            self.stagnation_counter = 0
            self.current_bounds = get_gain_bounds_for_pso(controller_type)

        def adapt_parameters(self, current_best_fitness: float) -> Dict[str, float]:
            """Adapt PSO parameters based on progress."""

            # Check for stagnation
            if (len(self.best_fitness_history) > 0 and
                abs(current_best_fitness - self.best_fitness_history[-1]) < 1e-6):
                self.stagnation_counter += 1
            else:
                self.stagnation_counter = 0

            self.best_fitness_history.append(current_best_fitness)

            # Adaptive parameter adjustment
            if self.stagnation_counter > 10:
                # Increase exploration
                w = 0.9  # High inertia
                c1, c2 = 2.5, 1.5  # High cognitive, low social

                # Expand search bounds slightly
                lower, upper = self.current_bounds
                expansion = 0.1
                self.current_bounds = (
                    [l * (1 - expansion) for l in lower],
                    [u * (1 + expansion) for u in upper]
                )

            elif self.iteration < 50:
                # Early exploration phase
                w = 0.9
                c1, c2 = 2.0, 2.0
            else:
                # Late exploitation phase
                w = 0.4
                c1, c2 = 1.5, 2.5

            self.iteration += 1

            return {
                'w': w,
                'c1': c1,
                'c2': c2,
                'bounds': self.current_bounds
            }

        def fitness_function(self, gains: np.ndarray) -> float:
            """Adaptive fitness function with dynamic objectives."""

            try:
                controller = factory(gains)
                metrics = evaluate_controller_performance(controller)

                # Dynamic objective weighting based on iteration
                if self.iteration < 30:
                    # Early phase: focus on basic performance
                    return 0.7 * metrics['ise'] + 0.3 * metrics['control_effort']
                elif self.iteration < 80:
                    # Middle phase: balance performance and robustness
                    return (0.4 * metrics['ise'] +
                           0.3 * metrics['control_effort'] +
                           0.3 * metrics['robustness_penalty'])
                else:
                    # Late phase: focus on refinement
                    return (0.3 * metrics['ise'] +
                           0.2 * metrics['control_effort'] +
                           0.3 * metrics['robustness_penalty'] +
                           0.2 * metrics['chattering_penalty'])

            except:
                return float('inf')

    # Run adaptive PSO
    adaptive_controller = AdaptivePSOController()

    # Initial PSO configuration
    pso_params = adaptive_controller.adapt_parameters(float('inf'))

    optimizer = PSOTuner(
        controller_factory=adaptive_controller.fitness_function,
        config=config,
        adaptive_callback=adaptive_controller.adapt_parameters
    )

    return optimizer.optimize_adaptive()