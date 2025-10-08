# Example from: docs\factory\pso_integration_workflow.md
# Index: 1
# Runnable: False
# Hash: cea235e1

# example-metadata:
# runnable: false

class PSOFactoryInterface:
    """
    Specialized interface for PSO optimization integration.

    Features:
    - Vectorized controller creation for swarm populations
    - Automatic parameter validation and bounds checking
    - Performance-optimized fitness evaluation
    - Thread-safe parallel optimization support
    """

    def __init__(self, controller_type: str, plant_config: Any):
        self.controller_type = controller_type
        self.plant_config = plant_config
        self._setup_optimization_environment()

    def _setup_optimization_environment(self) -> None:
        """Initialize PSO optimization environment."""

        # Get controller specifications
        self.gain_spec = SMC_GAIN_SPECS[SMCType(self.controller_type)]
        self.n_gains = self.gain_spec.n_gains
        self.bounds = self.gain_spec.gain_bounds

        # Performance monitoring
        self.evaluation_count = 0
        self.successful_evaluations = 0
        self.failed_evaluations = 0

        # Thread-safe operations
        self._lock = threading.RLock()

    def create_pso_controller_factory(self) -> Callable[[GainsArray], PSOControllerWrapper]:
        """
        Create PSO-optimized controller factory function.

        Returns:
            Factory function that takes gains and returns PSO-wrapped controller
        """

        def controller_factory(gains: GainsArray) -> PSOControllerWrapper:
            """PSO controller factory with comprehensive validation."""

            with self._lock:
                self.evaluation_count += 1

                try:
                    # Validate gains
                    if not self._validate_pso_gains(gains):
                        self.failed_evaluations += 1
                        return self._create_fallback_controller(gains)

                    # Create controller via factory
                    controller = create_controller(
                        controller_type=self.controller_type,
                        config=self.plant_config,
                        gains=gains
                    )

                    # Wrap for PSO optimization
                    wrapper = PSOControllerWrapper(
                        controller=controller,
                        controller_type=self.controller_type,
                        validation_enabled=True
                    )

                    # Add PSO-required attributes
                    wrapper.n_gains = self.n_gains
                    wrapper.controller_type = self.controller_type
                    wrapper.max_force = getattr(controller, 'max_force', 150.0)

                    self.successful_evaluations += 1
                    return wrapper

                except Exception as e:
                    logger.warning(f"PSO controller creation failed: {e}")
                    self.failed_evaluations += 1
                    return self._create_fallback_controller(gains)

        # Add PSO-required attributes to factory function
        controller_factory.n_gains = self.n_gains
        controller_factory.controller_type = self.controller_type
        controller_factory.bounds = self.bounds
        controller_factory.max_force = 150.0

        return controller_factory

    def _validate_pso_gains(self, gains: GainsArray) -> bool:
        """Validate gains for PSO optimization."""
        try:
            gains_array = np.asarray(gains)

            # Check dimensions
            if len(gains_array) != self.n_gains:
                return False

            # Check bounds
            for i, (gain, (min_val, max_val)) in enumerate(zip(gains_array, self.bounds)):
                if not (min_val <= gain <= max_val):
                    return False

            # Check numerical validity
            if not np.all(np.isfinite(gains_array)):
                return False

            # Controller-specific validation
            return validate_smc_gains(SMCType(self.controller_type), gains_array)

        except Exception:
            return False

    def _create_fallback_controller(self, gains: GainsArray) -> PSOControllerWrapper:
        """Create fallback controller for invalid parameters."""

        # Use default gains as fallback
        default_gains = get_default_gains(self.controller_type)

        try:
            controller = create_controller(
                controller_type=self.controller_type,
                config=self.plant_config,
                gains=default_gains
            )

            wrapper = PSOControllerWrapper(
                controller=controller,
                controller_type=self.controller_type,
                validation_enabled=False  # Disable validation for fallback
            )

            wrapper.n_gains = self.n_gains
            wrapper.controller_type = self.controller_type
            wrapper.is_fallback = True

            return wrapper

        except Exception:
            # Emergency fallback - return minimal controller
            return self._create_emergency_fallback()

    def get_optimization_statistics(self) -> Dict[str, Any]:
        """Get PSO optimization statistics."""
        with self._lock:
            success_rate = self.successful_evaluations / max(1, self.evaluation_count)
            return {
                'total_evaluations': self.evaluation_count,
                'successful_evaluations': self.successful_evaluations,
                'failed_evaluations': self.failed_evaluations,
                'success_rate': success_rate,
                'optimization_health': 'GOOD' if success_rate > 0.8 else 'WARNING' if success_rate > 0.5 else 'POOR'
            }