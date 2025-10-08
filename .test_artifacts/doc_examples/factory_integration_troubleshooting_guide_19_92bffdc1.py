# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 19
# Runnable: False
# Hash: 92bffdc1

# example-metadata:
# runnable: false

class OptimizedControllerFactory:
    """Optimized controller factory with caching and pooling."""

    def __init__(self):
        self._config_cache = {}
        self._controller_pool = {}
        self._pool_size = 10

    def _get_cached_config(self, controller_type, config_key):
        """Get cached configuration to avoid repeated processing."""

        cache_key = (controller_type, config_key)

        if cache_key not in self._config_cache:
            # Create and cache configuration
            if config_key is None:
                # Use defaults
                from src.controllers.factory import get_default_gains
                gains = get_default_gains(controller_type)
                config_obj = self._create_minimal_config(controller_type, gains)
            else:
                # Process provided configuration
                config_obj = self._process_config(controller_type, config_key)

            self._config_cache[cache_key] = config_obj

        return self._config_cache[cache_key]

    def _create_minimal_config(self, controller_type, gains):
        """Create minimal configuration object."""

        from src.controllers.factory import CONTROLLER_REGISTRY

        controller_info = CONTROLLER_REGISTRY[controller_type]
        config_class = controller_info['config_class']

        # Minimal required parameters
        if controller_type == 'classical_smc':
            return config_class(
                gains=gains,
                max_force=150.0,
                boundary_layer=0.02,
                dt=0.001
            )
        elif controller_type == 'adaptive_smc':
            return config_class(
                gains=gains,
                max_force=150.0,
                dt=0.001
            )
        # ... other controller types

    def create_optimized_controller(self, controller_type, gains=None, config=None):
        """Create controller with optimization."""

        # Use pooling for identical configurations
        pool_key = (controller_type, tuple(gains) if gains else None)

        if pool_key in self._controller_pool:
            # Reuse existing controller
            controller = self._controller_pool[pool_key]
            controller.reset()  # Reset state
            return controller

        # Create new controller
        if gains is not None:
            controller = create_controller(controller_type, gains=gains)
        else:
            controller = create_controller(controller_type, config=config)

        # Add to pool if space available
        if len(self._controller_pool) < self._pool_size:
            self._controller_pool[pool_key] = controller

        return controller

    def clear_cache(self):
        """Clear all caches to free memory."""
        self._config_cache.clear()
        self._controller_pool.clear()

# Usage
factory = OptimizedControllerFactory()

# Create controllers efficiently
controllers = []
for i in range(100):
    gains = [20.0 + i*0.1, 15.0, 12.0, 8.0, 35.0, 5.0]
    controller = factory.create_optimized_controller('classical_smc', gains=gains)
    controllers.append(controller)

# Cleanup
factory.clear_cache()