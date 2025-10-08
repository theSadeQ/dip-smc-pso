# Example from: docs\technical\mathematical_foundations.md
# Index: 7
# Runnable: False
# Hash: 648700cb

class PSOOptimizedFactory:
    """Factory with integrated PSO optimization."""

    def __init__(self, controller_type: str):
        self.controller_type = controller_type
        self.bounds = self._get_theoretical_bounds()

    def _get_theoretical_bounds(self) -> Tuple[List[float], List[float]]:
        """Get theoretically motivated gain bounds."""

        if self.controller_type == 'classical_smc':
            # Based on pole placement and bandwidth requirements
            lower = [0.1, 0.1, 0.1, 0.1, 1.0, 0.0]  # [c1, c2, λ1, λ2, K, kd]
            upper = [50.0, 50.0, 50.0, 50.0, 200.0, 50.0]

        elif self.controller_type == 'sta_smc':
            # Based on finite-time convergence requirements
            lower = [1.0, 0.5, 0.1, 0.1, 0.1, 0.1]  # [K1, K2, c1, λ1, c2, λ2]
            upper = [100.0, 99.0, 50.0, 50.0, 50.0, 50.0]  # Ensure K1 > K2

        return lower, upper

    def optimize_gains(self, plant_model, cost_function, n_particles=30, n_iterations=100):
        """Optimize controller gains using PSO."""

        # Initialize PSO with theoretical bounds
        pso = PSOOptimizer(
            bounds=self.bounds,
            n_particles=n_particles,
            n_iterations=n_iterations
        )

        # Define fitness function
        def fitness(gains):
            try:
                # Create controller with gains
                controller = create_controller(self.controller_type, gains=gains)

                # Validate stability before simulation
                if not self._validate_stability(gains):
                    return float('inf')

                # Simulate and compute cost
                cost = simulate_and_evaluate(controller, plant_model, cost_function)
                return cost

            except Exception:
                return float('inf')

        # Run optimization
        optimal_gains, optimal_cost = pso.optimize(fitness)

        return optimal_gains, optimal_cost