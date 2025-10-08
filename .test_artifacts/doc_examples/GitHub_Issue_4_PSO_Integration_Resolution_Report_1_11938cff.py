# Example from: docs\GitHub_Issue_4_PSO_Integration_Resolution_Report.md
# Index: 1
# Runnable: False
# Hash: 11938cff

class PSOTuner:
    """
    Rebuilt PSO optimization engine with robust controller integration.

    Key Improvements:
    - Unified controller factory interface
    - Dynamic parameter count adaptation
    - Enhanced bounds management
    - Improved convergence monitoring
    """

    def __init__(self, controller_factory: Callable, config: dict, seed: int = 42):
        """
        Initialize PSO tuner with enhanced validation and error handling.

        Args:
            controller_factory: Factory function with n_gains attribute
            config: Complete configuration with PSO parameters
            seed: Random seed for reproducible optimization
        """
        # Robust parameter extraction with fallbacks
        self.pso_config = config.get('pso', {})
        self.controller_factory = controller_factory

        # Enhanced parameter count detection
        self.n_gains = getattr(controller_factory, 'n_gains', 6)

        # Dynamic bounds adaptation
        self.bounds = self._extract_bounds(config)

        # Validation and safety checks
        self._validate_configuration()