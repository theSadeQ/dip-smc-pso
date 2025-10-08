# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 21
# Runnable: False
# Hash: 282d1bb4

import gc
import weakref

class ManagedControllerFactory:
    """Controller factory with explicit memory management."""

    def __init__(self):
        self._weak_references = set()
        self._creation_count = 0
        self._cleanup_threshold = 100

    def create_managed_controller(self, controller_type, **kwargs):
        """Create controller with memory management."""

        # Create controller
        controller = create_controller(controller_type, **kwargs)

        # Add weak reference for tracking
        weak_ref = weakref.ref(controller, self._on_controller_deleted)
        self._weak_references.add(weak_ref)

        self._creation_count += 1

        # Periodic cleanup
        if self._creation_count % self._cleanup_threshold == 0:
            self._perform_cleanup()

        return controller

    def _on_controller_deleted(self, weak_ref):
        """Callback when controller is garbage collected."""
        self._weak_references.discard(weak_ref)

    def _perform_cleanup(self):
        """Perform explicit cleanup."""

        # Remove dead weak references
        dead_refs = set()
        for ref in self._weak_references:
            if ref() is None:
                dead_refs.add(ref)

        self._weak_references -= dead_refs

        # Force garbage collection
        gc.collect()

        print(f"Cleanup: {len(self._weak_references)} controllers active, "
              f"{self._creation_count} total created")

    def get_active_controller_count(self):
        """Get number of active controllers."""
        return len([ref for ref in self._weak_references if ref() is not None])

    def force_cleanup(self):
        """Force immediate cleanup."""
        self._perform_cleanup()

# Usage with managed factory
managed_factory = ManagedControllerFactory()

# PSO with memory management
def managed_pso_fitness(gains):
    """PSO fitness function with memory management."""

    controller = managed_factory.create_managed_controller('classical_smc', gains=gains)

    try:
        # Evaluate controller
        performance = evaluate_controller_performance(controller)
        return performance['total_cost']

    finally:
        # Explicit cleanup
        del controller

        # Periodic forced cleanup
        if managed_factory._creation_count % 50 == 0:
            managed_factory.force_cleanup()

# Run PSO with memory management
# ... PSO optimization code