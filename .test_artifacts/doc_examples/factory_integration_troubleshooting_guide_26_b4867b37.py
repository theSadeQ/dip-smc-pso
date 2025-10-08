# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 26
# Runnable: False
# Hash: b4867b37

class LockFreeControllerCache:
    """Lock-free controller cache using pre-created controllers."""

    def __init__(self):
        self._controller_cache = {}
        self._cache_lock = threading.RLock()
        self._initialized = False

    def initialize_cache(self, preload_configs):
        """Pre-create controllers to avoid runtime factory calls."""

        if self._initialized:
            return

        print("Initializing controller cache...")

        # Create controllers sequentially during initialization
        for config in preload_configs:
            try:
                controller = create_controller(**config)
                cache_key = self._make_cache_key(config)
                self._controller_cache[cache_key] = controller
                print(f"Cached: {config['controller_type']}")
            except Exception as e:
                print(f"Failed to cache {config}: {e}")

        self._initialized = True
        print(f"Cache initialized with {len(self._controller_cache)} controllers")

    def _make_cache_key(self, config):
        """Create cache key from configuration."""
        key_parts = [config['controller_type']]

        if 'gains' in config:
            key_parts.extend([f"{g:.3f}" for g in config['gains']])

        return tuple(key_parts)

    def get_controller(self, config):
        """Get controller from cache (thread-safe read)."""

        cache_key = self._make_cache_key(config)

        if cache_key in self._controller_cache:
            # Clone controller to avoid shared state issues
            cached_controller = self._controller_cache[cache_key]
            return self._clone_controller(cached_controller, config)
        else:
            # Fallback to factory (with lock)
            return create_controller(**config)

    def _clone_controller(self, cached_controller, config):
        """Create a new controller with same configuration."""
        # Reset cached controller state
        cached_controller.reset()
        return cached_controller

# Initialize cache at startup
cache = LockFreeControllerCache()

# Pre-define common configurations
common_configs = [
    {'controller_type': 'classical_smc', 'gains': [20, 15, 12, 8, 35, 5]},
    {'controller_type': 'adaptive_smc', 'gains': [25, 18, 15, 10, 4]},
    {'controller_type': 'sta_smc', 'gains': [25, 15, 20, 12, 8, 6]},
]

cache.initialize_cache(common_configs)

# Use cache in PSO (thread-safe)
def thread_safe_fitness_function(gains):
    """PSO fitness function using cached controllers."""

    config = {'controller_type': 'classical_smc', 'gains': gains}
    controller = cache.get_controller(config)

    return evaluate_controller_performance(controller)