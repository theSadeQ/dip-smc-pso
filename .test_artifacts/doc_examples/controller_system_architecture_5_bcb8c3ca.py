# Example from: docs\architecture\controller_system_architecture.md
# Index: 5
# Runnable: False
# Hash: bcb8c3ca

class PSOOptimizer:
    """
    Universal PSO optimizer for all SMC controller types.

    Provides consistent optimization interface with controller-specific
    fitness functions, boundary handling, and convergence criteria.
    """

    def __init__(
        self,
        controller_type: str,
        config: Dict[str, Any],
        dynamics_config: Dict[str, Any]
    ):
        self.controller_type = controller_type
        self.bounds = self._get_controller_bounds(controller_type)
        self.fitness_evaluator = self._create_fitness_evaluator(
            controller_type, config, dynamics_config
        )

    def optimize(
        self,
        n_particles: int = 30,
        max_iterations: int = 100,
        convergence_threshold: float = 1e-6
    ) -> OptimizationResult:
        """Run PSO optimization with adaptive parameters."""

        # Initialize swarm with controller-specific bounds
        swarm = self._initialize_swarm(n_particles)

        # PSO main loop with adaptive parameters
        for iteration in range(max_iterations):
            # Evaluate fitness for all particles
            fitness_values = self._evaluate_population(swarm)

            # Update global and personal bests
            self._update_bests(swarm, fitness_values)

            # Check convergence
            if self._check_convergence(fitness_values, convergence_threshold):
                break

            # Update particle velocities and positions
            self._update_swarm(swarm, iteration, max_iterations)

        return self._create_optimization_result(swarm, iteration)