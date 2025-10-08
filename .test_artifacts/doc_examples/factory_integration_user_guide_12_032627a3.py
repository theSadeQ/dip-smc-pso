# Example from: docs\factory\factory_integration_user_guide.md
# Index: 12
# Runnable: True
# Hash: 032627a3

from src.controllers.factory import create_controller, list_available_controllers

class AdaptiveControllerManager:
    """Dynamically switch between controller types based on performance."""

    def __init__(self, config):
        self.config = config
        self.controllers = {}
        self.current_controller = None

        # Pre-create all available controllers
        for controller_type in list_available_controllers():
            try:
                self.controllers[controller_type] = create_controller(
                    controller_type, config=config
                )
            except Exception as e:
                print(f"Failed to create {controller_type}: {e}")

    def select_best_controller(self, performance_metrics):
        """Select controller based on performance metrics."""
        best_type = self._evaluate_performance(performance_metrics)
        self.current_controller = self.controllers[best_type]
        return self.current_controller

    def _evaluate_performance(self, metrics):
        # Implementation specific to performance criteria
        pass