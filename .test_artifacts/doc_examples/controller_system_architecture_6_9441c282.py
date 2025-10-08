# Example from: docs\architecture\controller_system_architecture.md
# Index: 6
# Runnable: False
# Hash: 9441c282

# example-metadata:
# runnable: false

class FitnessEvaluator:
    """Controller-specific fitness evaluation strategies."""

    def __init__(self, controller_type: str, config: Dict[str, Any]):
        self.controller_type = controller_type
        self.config = config
        self.dynamics = self._create_dynamics(config['dynamics'])

    def evaluate_fitness(self, gains: List[float]) -> float:
        """Evaluate controller performance with given gains."""

        try:
            # Create controller with candidate gains
            controller = create_controller(
                self.controller_type,
                config=self.config,
                gains=gains
            )

            # Run simulation
            simulation_result = self._run_simulation(controller)

            # Compute comprehensive fitness
            fitness = self._compute_fitness_score(simulation_result)

            return fitness

        except Exception as e:
            # Penalty for invalid configurations
            return 1e6  # Large penalty value

    def _compute_fitness_score(self, result: SimulationResult) -> float:
        """Compute multi-objective fitness score."""

        # Weighted combination of performance metrics
        weights = {
            'angle_error': 0.4,      # Pendulum stabilization
            'position_error': 0.2,   # Cart positioning
            'control_effort': 0.2,   # Energy efficiency
            'settling_time': 0.1,    # Response speed
            'overshoot': 0.1        # Stability margin
        }

        metrics = self._extract_performance_metrics(result)

        fitness = sum(
            weights[metric] * self._normalize_metric(metric, value)
            for metric, value in metrics.items()
        )

        return fitness