# Example from: docs\testing\reports\2025-09-30\technical\resolution_roadmap.md
# Index: 7
# Runnable: False
# Hash: 51d0fbe3

# File: src/controllers/factory/memory_managed_factory.py
class MemoryManagedFactory:
    """Controller factory with automatic memory management."""

    def __init__(self):
        self._controller_pool = {}           # Reusable controller instances
        self._memory_monitor = MemoryMonitor()

    def create_controller(self, controller_type: str, config: dict) -> Controller:
        """Create controller with memory tracking."""
        with self._memory_monitor.track_creation():
            # Check for reusable instance
            controller_key = self._compute_controller_key(controller_type, config)

            if controller_key in self._controller_pool:
                controller = self._controller_pool[controller_key]
                controller.reset_state()  # Reset instead of recreate
                return controller

            # Create new instance with monitoring
            controller = self._create_new_controller(controller_type, config)
            self._controller_pool[controller_key] = controller

            return controller

    def cleanup_unused_controllers(self):
        """Cleanup controllers not used recently."""
        current_time = time.time()
        to_remove = []

        for key, controller in self._controller_pool.items():
            if current_time - controller.last_used > CONTROLLER_TIMEOUT:
                controller._cleanup_resources()
                to_remove.append(key)

        for key in to_remove:
            del self._controller_pool[key]