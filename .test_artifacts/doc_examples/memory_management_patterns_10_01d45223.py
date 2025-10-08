# Example from: docs\memory_management_patterns.md
# Index: 10
# Runnable: True
# Hash: 01d45223

import time
import gc

class ControllerManager:
    def __init__(self, controller_type, **kwargs):
        from src.controllers.factory import create_controller
        self.controller = create_controller(controller_type, **kwargs)
        self.created_at = time.time()
        self.max_lifetime_hours = 24

    def should_recreate(self):
        """Recreate controller every 24 hours to prevent memory accumulation."""
        lifetime_hours = (time.time() - self.created_at) / 3600
        return lifetime_hours > self.max_lifetime_hours

    def refresh(self):
        """Safely recreate controller."""
        from src.controllers.factory import create_controller
        controller_type = type(self.controller).__name__.lower()

        old_controller = self.controller
        self.controller = create_controller(controller_type, **self.get_controller_params())
        old_controller.cleanup()
        del old_controller
        gc.collect()
        self.created_at = time.time()

    def get_controller_params(self):
        """Extract controller parameters for recreation."""
        return {
            'gains': self.controller.gains,
            'max_force': self.controller.max_force,
            # Add other controller-specific parameters
        }