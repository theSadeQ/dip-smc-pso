# Example from: docs\configuration_schema_validation.md
# Index: 15
# Runnable: False
# Hash: ce49c01c

# example-metadata:
# runnable: false

class ConfigurationHotReloader:
    """Hot-reload configuration with validation."""

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.current_config = None
        self.validator = None
        self.reload_config()

    def reload_config(self) -> bool:
        """Reload and validate configuration file."""
        try:
            # Load new configuration
            with open(self.config_file, 'r') as f:
                new_config_data = yaml.safe_load(f)

            # Validate new configuration
            new_config = MasterConfig(**new_config_data)

            # Cross-validate with current system state
            if self.current_config:
                self._validate_config_transition(self.current_config, new_config)

            # Update current configuration
            self.current_config = new_config
            self.validator = RuntimeConfigValidator(new_config.dict())

            return True

        except Exception as e:
            raise ConfigurationError(f"Configuration reload failed: {e}")

    def _validate_config_transition(self, old_config: MasterConfig, new_config: MasterConfig) -> None:
        """Validate transition between configurations."""

        # Critical parameters that shouldn't change during operation
        critical_params = [
            'physics.pendulum_length_1',
            'physics.pendulum_length_2',
            'physics.cart_mass',
            'system.environment'
        ]

        for param_path in critical_params:
            old_value = self._get_config_value(old_config.dict(), param_path)
            new_value = self._get_config_value(new_config.dict(), param_path)

            if old_value != new_value:
                raise ValueError(f"Critical parameter {param_path} cannot change during operation")

    def _get_config_value(self, config: dict, path: str) -> any:
        """Get configuration value by path."""
        current = config
        for part in path.split('.'):
            current = current[part]
        return current