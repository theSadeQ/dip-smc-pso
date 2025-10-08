# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 29
# Runnable: True
# Hash: 31d737b9

#!/usr/bin/env python3
"""Best practices for robust factory integration."""

class RobustFactoryIntegration:
    """Demonstrates best practices for factory integration."""

    def __init__(self):
        self.factory_cache = {}
        self.validation_cache = {}

    def create_controller_robust(self, controller_type, **kwargs):
        """Create controller with comprehensive robustness patterns."""

        # 1. Input validation
        if not self._validate_inputs(controller_type, kwargs):
            raise ValueError("Invalid inputs")

        # 2. Pre-creation checks
        if not self._pre_creation_checks(controller_type):
            raise ImportError(f"Controller {controller_type} not available")

        # 3. Safe creation with fallbacks
        try:
            return self._create_with_fallbacks(controller_type, kwargs)
        except Exception as e:
            self._log_creation_failure(controller_type, kwargs, e)
            raise

    def _validate_inputs(self, controller_type, kwargs):
        """Validate inputs before creation."""

        # Check controller type
        if not isinstance(controller_type, str) or not controller_type.strip():
            return False

        # Check gains if provided
        if 'gains' in kwargs:
            gains = kwargs['gains']

            if not isinstance(gains, (list, tuple)):
                return False

            if not all(isinstance(g, (int, float)) for g in gains):
                return False

            if not all(g > 0 for g in gains):
                return False

        return True

    def _pre_creation_checks(self, controller_type):
        """Perform pre-creation availability checks."""

        try:
            from src.controllers.factory import list_available_controllers
            available = list_available_controllers()
            return controller_type in available
        except Exception:
            return False

    def _create_with_fallbacks(self, controller_type, kwargs):
        """Create controller with fallback strategies."""

        strategies = [
            self._strategy_direct_creation,
            self._strategy_minimal_config,
            self._strategy_default_parameters
        ]

        last_exception = None

        for strategy in strategies:
            try:
                return strategy(controller_type, kwargs)
            except Exception as e:
                last_exception = e
                continue

        # All strategies failed
        raise last_exception

    def _strategy_direct_creation(self, controller_type, kwargs):
        """Strategy 1: Direct creation with provided parameters."""
        from src.controllers.factory import create_controller
        return create_controller(controller_type, **kwargs)

    def _strategy_minimal_config(self, controller_type, kwargs):
        """Strategy 2: Minimal configuration creation."""

        # Use only essential parameters
        essential_params = {}

        if 'gains' in kwargs:
            essential_params['gains'] = kwargs['gains']

        # Add required defaults
        if controller_type == 'classical_smc':
            essential_params.update({
                'max_force': 150.0,
                'boundary_layer': 0.02,
                'dt': 0.001
            })
        elif controller_type == 'adaptive_smc':
            essential_params.update({
                'max_force': 150.0,
                'dt': 0.001
            })

        from src.controllers.factory import create_controller
        return create_controller(controller_type, **essential_params)

    def _strategy_default_parameters(self, controller_type, kwargs):
        """Strategy 3: Use all default parameters."""

        from src.controllers.factory import create_controller
        return create_controller(controller_type)

    def _log_creation_failure(self, controller_type, kwargs, exception):
        """Log creation failure for debugging."""

        import logging
        logger = logging.getLogger(__name__)

        logger.error(f"Controller creation failed:")
        logger.error(f"  Type: {controller_type}")
        logger.error(f"  Parameters: {kwargs}")
        logger.error(f"  Exception: {exception}")

# Validation patterns
class FactoryValidationPatterns:
    """Common validation patterns for factory integration."""

    @staticmethod
    def validate_controller_type(controller_type):
        """Validate controller type string."""
        if not isinstance(controller_type, str):
            raise TypeError("Controller type must be string")

        if not controller_type.strip():
            raise ValueError("Controller type cannot be empty")

        # Normalize
        return controller_type.strip().lower()

    @staticmethod
    def validate_gains(gains, expected_count=None):
        """Validate gain array."""

        if gains is None:
            return True  # Allow None for default gains

        # Convert numpy arrays
        if hasattr(gains, 'tolist'):
            gains = gains.tolist()

        if not isinstance(gains, (list, tuple)):
            raise TypeError("Gains must be list or tuple")

        if len(gains) == 0:
            raise ValueError("Gains cannot be empty")

        # Check types
        if not all(isinstance(g, (int, float)) for g in gains):
            raise TypeError("All gains must be numeric")

        # Check finite values
        import numpy as np
        if not all(np.isfinite(g) for g in gains):
            raise ValueError("All gains must be finite")

        # Check positivity
        if not all(g > 0 for g in gains):
            raise ValueError("All gains must be positive")

        # Check count if specified
        if expected_count is not None and len(gains) != expected_count:
            raise ValueError(f"Expected {expected_count} gains, got {len(gains)}")

        return True

    @staticmethod
    def validate_configuration(config, controller_type):
        """Validate configuration object."""

        if config is None:
            return True  # Allow None for default config

        # Check for required attributes based on controller type
        if controller_type == 'classical_smc':
            required_attrs = ['max_force', 'boundary_layer']
            for attr in required_attrs:
                if hasattr(config, attr):
                    value = getattr(config, attr)
                    if not isinstance(value, (int, float)) or value <= 0:
                        raise ValueError(f"Invalid {attr}: {value}")

        return True

# Testing patterns
class FactoryTestingPatterns:
    """Testing patterns for factory integration."""

    def test_all_controllers(self):
        """Test all available controllers."""

        from src.controllers.factory import list_available_controllers

        results = {}
        available = list_available_controllers()

        for controller_type in available:
            try:
                # Test with defaults
                controller = create_controller(controller_type)
                results[controller_type] = {'default': 'success'}

                # Test with custom gains
                from src.controllers.factory import get_default_gains
                custom_gains = [g * 1.1 for g in get_default_gains(controller_type)]
                controller = create_controller(controller_type, gains=custom_gains)
                results[controller_type]['custom_gains'] = 'success'

            except Exception as e:
                results[controller_type] = {'error': str(e)}

        return results

    def stress_test_factory(self, n_iterations=1000):
        """Stress test factory with many creations."""

        import time

        start_time = time.time()
        errors = []

        for i in range(n_iterations):
            try:
                controller = create_controller('classical_smc')
                del controller  # Explicit cleanup
            except Exception as e:
                errors.append((i, str(e)))

        end_time = time.time()

        return {
            'total_time': end_time - start_time,
            'avg_time_per_creation': (end_time - start_time) / n_iterations,
            'errors': errors,
            'success_rate': (n_iterations - len(errors)) / n_iterations
        }

# Usage examples
if __name__ == "__main__":
    # Robust factory integration
    robust_factory = RobustFactoryIntegration()

    try:
        controller = robust_factory.create_controller_robust(
            'classical_smc',
            gains=[20, 15, 12, 8, 35, 5]
        )
        print("✅ Robust controller creation successful")
    except Exception as e:
        print(f"❌ Robust controller creation failed: {e}")

    # Validation patterns
    try:
        FactoryValidationPatterns.validate_gains([20, 15, 12, 8, 35, 5], expected_count=6)
        print("✅ Gain validation passed")
    except Exception as e:
        print(f"❌ Gain validation failed: {e}")

    # Testing patterns
    tester = FactoryTestingPatterns()
    test_results = tester.test_all_controllers()
    print(f"Controller test results: {test_results}")