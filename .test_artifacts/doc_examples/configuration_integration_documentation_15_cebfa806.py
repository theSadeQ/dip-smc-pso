# Example from: docs\configuration_integration_documentation.md
# Index: 15
# Runnable: True
# Hash: cebfa806

import os
from typing import Dict, Any, Optional

class EnvironmentConfigurationManager:
    """Manage environment-based configuration overrides."""

    def __init__(self, base_config_file: str = "config.yaml"):
        self.base_config = self._load_base_config(base_config_file)
        self.environment = os.getenv('DIP_ENV', 'development')
        self.env_overrides = self._load_environment_overrides()

    def _load_base_config(self, config_file: str):
        """Load base configuration."""
        from src.config import load_config
        return load_config(config_file)

    def _load_environment_overrides(self) -> Dict[str, Any]:
        """Load environment-specific overrides."""

        env_configs = {
            'development': {
                'simulation': {'duration': 2.0},  # Shorter for testing
                'logging': {'level': 'DEBUG'},
                'pso': {'n_particles': 10, 'max_iter': 20}  # Faster optimization
            },
            'testing': {
                'simulation': {'duration': 1.0, 'dt': 0.01},  # Fast testing
                'logging': {'level': 'WARNING'},
                'controllers': {
                    'classical_smc': {'gains': [10, 8, 6, 4, 20, 2]}  # Conservative gains
                }
            },
            'production': {
                'logging': {'level': 'INFO'},
                'monitoring': {'performance_tracking': True},
                'pso': {'n_particles': 50, 'max_iter': 200}  # Thorough optimization
            },
            'hil': {
                'hil': {'enabled': True},
                'simulation': {'dt': 0.001},  # High precision for HIL
                'controllers': {
                    'classical_smc': {'dt': 0.001}  # Match simulation timestep
                }
            }
        }

        return env_configs.get(self.environment, {})

    def get_merged_config(self) -> Any:
        """Get configuration with environment overrides applied."""

        merged_config = self._deep_merge(
            self._config_to_dict(self.base_config),
            self.env_overrides
        )

        # Apply environment variable overrides
        env_var_overrides = self._extract_env_var_overrides()
        if env_var_overrides:
            merged_config = self._deep_merge(merged_config, env_var_overrides)

        # Convert back to config object
        return self._dict_to_config(merged_config)

    def _extract_env_var_overrides(self) -> Dict[str, Any]:
        """Extract configuration overrides from environment variables."""

        overrides = {}

        # Environment variable patterns:
        # DIP_CONTROLLER_CLASSICAL_GAINS=20,15,12,8,35,5
        # DIP_SIMULATION_DURATION=5.0
        # DIP_PSO_N_PARTICLES=30

        for key, value in os.environ.items():
            if key.startswith('DIP_'):
                # Parse nested key: DIP_CONTROLLER_CLASSICAL_GAINS -> controllers.classical_smc.gains
                parts = key[4:].lower().split('_')  # Remove 'DIP_' prefix

                if len(parts) >= 2:
                    config_dict = overrides

                    # Navigate/create nested structure
                    for part in parts[:-1]:
                        if part not in config_dict:
                            config_dict[part] = {}
                        config_dict = config_dict[part]

                    # Set value with type conversion
                    final_key = parts[-1]
                    config_dict[final_key] = self._convert_env_value(value)

        return overrides

    def _convert_env_value(self, value: str) -> Any:
        """Convert environment variable string to appropriate type."""

        # Boolean conversion
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'

        # List conversion (comma-separated)
        if ',' in value:
            try:
                return [float(x.strip()) for x in value.split(',')]
            except ValueError:
                return [x.strip() for x in value.split(',')]

        # Numeric conversion
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass

        # String value
        return value

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""

        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _config_to_dict(self, config: Any) -> Dict[str, Any]:
        """Convert configuration object to dictionary."""

        if hasattr(config, 'model_dump'):
            return config.model_dump()
        elif hasattr(config, '__dict__'):
            return vars(config)
        else:
            return config

    def _dict_to_config(self, config_dict: Dict[str, Any]) -> Any:
        """Convert dictionary back to configuration object."""

        # Create a simple namespace object
        class ConfigNamespace:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    if isinstance(value, dict):
                        setattr(self, key, ConfigNamespace(**value))
                    else:
                        setattr(self, key, value)

        return ConfigNamespace(**config_dict)

# Usage
env_manager = EnvironmentConfigurationManager()

# Set environment
os.environ['DIP_ENV'] = 'production'
os.environ['DIP_PSO_N_PARTICLES'] = '40'
os.environ['DIP_CONTROLLER_CLASSICAL_GAINS'] = '22,16,14,9,38,5.5'

# Get merged configuration
config = env_manager.get_merged_config()

# Use with factory
controller = create_controller('classical_smc', config=config)