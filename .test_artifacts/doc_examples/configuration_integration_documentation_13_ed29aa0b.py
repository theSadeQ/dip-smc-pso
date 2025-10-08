# Example from: docs\configuration_integration_documentation.md
# Index: 13
# Runnable: True
# Hash: ed29aa0b

class DynamicConfigurationManager:
    """Manage dynamic configuration updates."""

    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
        self.controller_cache = {}
        self.observers = []

    def _load_config(self):
        """Load configuration from file."""
        from src.config import load_config
        return load_config(self.config_file)

    def update_controller_config(self, controller_type: str, **updates):
        """Update controller configuration dynamically."""

        # Update configuration
        if controller_type not in self.config.controllers:
            self.config.controllers[controller_type] = {}

        for key, value in updates.items():
            self.config.controllers[controller_type][key] = value

        # Invalidate cached controllers
        if controller_type in self.controller_cache:
            del self.controller_cache[controller_type]

        # Notify observers
        self._notify_observers(controller_type, updates)

    def get_controller(self, controller_type: str):
        """Get controller with current configuration."""

        if controller_type not in self.controller_cache:
            # Create controller with current config
            controller = create_controller(controller_type, config=self.config)
            self.controller_cache[controller_type] = controller

        return self.controller_cache[controller_type]

    def register_observer(self, callback):
        """Register configuration change observer."""
        self.observers.append(callback)

    def _notify_observers(self, controller_type: str, updates: Dict[str, Any]):
        """Notify observers of configuration changes."""
        for observer in self.observers:
            try:
                observer(controller_type, updates)
            except Exception as e:
                print(f"Observer notification failed: {e}")

    def save_config(self):
        """Save current configuration to file."""
        import yaml

        # Convert config to dictionary
        config_dict = self.config.model_dump() if hasattr(self.config, 'model_dump') else vars(self.config)

        with open(self.config_file, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)

# Usage
config_manager = DynamicConfigurationManager()

# Update configuration
config_manager.update_controller_config(
    'classical_smc',
    gains=[22, 16, 14, 9, 38, 5.5],
    max_force=160.0
)

# Get updated controller
controller = config_manager.get_controller('classical_smc')

# Register change observer
def config_change_handler(controller_type, updates):
    print(f"Configuration updated for {controller_type}: {updates}")

config_manager.register_observer(config_change_handler)