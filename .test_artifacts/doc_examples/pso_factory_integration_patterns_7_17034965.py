# Example from: docs\pso_factory_integration_patterns.md
# Index: 7
# Runnable: True
# Hash: 17034965

def memory_efficient_pso():
    """Memory-optimized PSO for large-scale optimization."""

    # Pattern 1: Reuse controller instances
    controller_pool = {}

    def pooled_factory(gains: np.ndarray, controller_type: SMCType):
        """Factory with controller pooling."""
        gains_key = tuple(gains)

        if gains_key not in controller_pool:
            # Create new controller only if not in pool
            controller_pool[gains_key] = create_smc_for_pso(controller_type, gains)

        return controller_pool[gains_key]

    # Pattern 2: Batch evaluation for parallel PSO
    def batch_fitness_evaluation(gains_batch: List[np.ndarray]) -> List[float]:
        """Evaluate multiple gain sets in batch."""

        # Create controllers in batch
        controllers = [
            create_smc_for_pso(SMCType.CLASSICAL, gains)
            for gains in gains_batch
        ]

        # Parallel evaluation
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(max_workers=4) as executor:
            fitness_values = list(executor.map(
                evaluate_controller_performance,
                controllers
            ))

        return [f['total_cost'] for f in fitness_values]

    # Pattern 3: Incremental evaluation
    class IncrementalEvaluator:
        """Incremental controller evaluation with caching."""

        def __init__(self, controller_type: SMCType):
            self.controller_type = controller_type
            self.evaluation_cache = {}
            self.factory = create_pso_controller_factory(controller_type)

        def evaluate(self, gains: np.ndarray) -> float:
            """Evaluate with caching."""
            gains_key = tuple(np.round(gains, 6))  # Round for cache efficiency

            if gains_key not in self.evaluation_cache:
                controller = self.factory(gains)
                performance = evaluate_controller_performance(controller)
                self.evaluation_cache[gains_key] = performance['total_cost']

            return self.evaluation_cache[gains_key]

        def clear_cache(self):
            """Clear evaluation cache to manage memory."""
            self.evaluation_cache.clear()