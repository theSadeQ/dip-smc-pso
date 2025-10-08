# Example from: docs\technical\controller_factory_integration.md
# Index: 19
# Runnable: False
# Hash: abf8c307

class ControllerPool:
    """Memory-efficient controller instance pool."""

    def __init__(self, max_instances: int = 100):
        self._pool = {}
        self._usage_count = {}
        self._max_instances = max_instances

    def get_controller(self, controller_type: str, config_hash: str):
        """Get controller from pool or create new one."""
        key = f"{controller_type}_{config_hash}"

        if key in self._pool:
            self._usage_count[key] += 1
            return self._pool[key]

        if len(self._pool) >= self._max_instances:
            self._evict_least_used()

        controller = create_controller(controller_type, config)
        self._pool[key] = controller
        self._usage_count[key] = 1
        return controller