# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 1
# Runnable: False
# Hash: 567fded4

class PSOFactoryInterface:
    """
    High-performance interface for PSO optimization workflows.

    Features:
    - Thread-safe parallel optimization
    - Automatic gain validation and bounds checking
    - Performance monitoring and diagnostics
    - Fallback mechanisms for invalid parameter sets
    """

    def __init__(self, controller_type: str, simulation_config: Any):
        self.controller_type = controller_type
        self.config = simulation_config
        self._initialize_pso_environment()

    def _initialize_pso_environment(self) -> None:
        """Setup PSO optimization environment with all requirements."""

        # Controller specifications
        self.registry_info = CONTROLLER_REGISTRY[self.controller_type]
        self.n_gains = self.registry_info['gain_count']
        self.default_gains = self.registry_info['default_gains']

        # PSO bounds (mathematically derived)
        self.bounds_lower, self.bounds_upper = get_gain_bounds_for_pso(
            SMCType(self.controller_type)
        )

        # Performance tracking
        self.metrics = {
            'total_evaluations': 0,
            'successful_evaluations': 0,
            'validation_failures': 0,
            'simulation_failures': 0,
            'best_fitness': float('inf'),
            'average_fitness': 0.0
        }

        # Thread safety
        self._evaluation_lock = threading.RLock()