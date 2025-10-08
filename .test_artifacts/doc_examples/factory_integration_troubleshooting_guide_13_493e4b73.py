# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 13
# Runnable: True
# Hash: 493e4b73

class OptimizedPSOWorkflow:
    """Optimized PSO workflow for maximum performance."""

    def __init__(self, smc_type, config):
        self.smc_type = smc_type
        self.config = config

        # Create factory once (expensive operation)
        self.factory = create_pso_controller_factory(smc_type, plant_config=config)

        # Pre-compute test scenarios
        self.test_scenarios = self._generate_test_scenarios()

        # Performance monitoring
        self.evaluation_count = 0
        self.evaluation_times = []

    def _generate_test_scenarios(self):
        """Pre-generate test scenarios for consistent evaluation."""
        import numpy as np

        scenarios = []

        # Standard test points
        test_states = [
            np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0]),  # Small angle
            np.array([0.3, 0.2, 0.0, 0.0, 0.0, 0.0]),   # Medium angle
            np.array([0.0, 0.0, 0.1, 0.0, 0.0, 0.0]),   # Cart displacement
        ]

        for state in test_states:
            scenarios.append({
                'initial_state': state,
                'simulation_time': 2.0,
                'target_state': np.zeros(6)
            })

        return scenarios

    def fast_fitness_function(self, gains):
        """Optimized fitness function for PSO."""
        import time
        start_time = time.time()

        try:
            # Quick validation
            if not validate_smc_gains(self.smc_type, gains):
                return float('inf')

            # Create controller (fast operation with pre-created factory)
            controller = self.factory(gains)

            # Fast performance evaluation
            total_cost = 0.0

            for scenario in self.test_scenarios:
                # Simplified simulation
                state = scenario['initial_state'].copy()
                cost = 0.0

                for _ in range(10):  # Short simulation steps
                    control_output = controller.compute_control(state, 0.0, {})
                    control_value = control_output.u if hasattr(control_output, 'u') else control_output

                    # Simple cost computation
                    state_cost = np.sum(state[:4]**2)  # Position and angle errors
                    control_cost = 0.1 * control_value**2
                    cost += state_cost + control_cost

                    # Simple state update (for speed)
                    state += 0.01 * np.random.randn(6) * 0.1  # Simplified dynamics

                total_cost += cost

            # Performance monitoring
            self.evaluation_count += 1
            elapsed = time.time() - start_time
            self.evaluation_times.append(elapsed)

            if self.evaluation_count % 100 == 0:
                avg_time = np.mean(self.evaluation_times[-100:])
                print(f"Evaluation {self.evaluation_count}: {avg_time:.4f}s avg")

            return total_cost

        except Exception as e:
            return float('inf')

    def run_optimization(self):
        """Run optimized PSO."""

        from src.optimization.algorithms.pso_optimizer import PSOTuner

        # Optimized PSO parameters
        pso_config = {
            'n_particles': 20,      # Smaller swarm for speed
            'max_iter': 50,         # Fewer iterations
            'w': 0.9,
            'c1': 2.0,
            'c2': 2.0,
            'early_stopping': True,
            'patience': 10
        }

        tuner = PSOTuner(
            controller_factory=self.fast_fitness_function,
            config=self.config,
            **pso_config
        )

        return tuner.optimize()

# Usage
optimizer = OptimizedPSOWorkflow(SMCType.CLASSICAL, config)
best_gains, best_fitness = optimizer.run_optimization()