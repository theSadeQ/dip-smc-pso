# Example from: docs\architecture\controller_system_architecture.md
# Index: 9
# Runnable: False
# Hash: ccda8d44

# example-metadata:
# runnable: false

class ConfigurationInterface:
    """Standardized configuration management across all components."""

    @classmethod
    def load_config(
        cls,
        config_path: str,
        schema_validation: bool = True
    ) -> Dict[str, Any]:
        """Load and validate configuration from YAML file."""

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        if schema_validation:
            cls._validate_schema(config)

        return config

    @classmethod
    def _validate_schema(cls, config: Dict[str, Any]) -> None:
        """Validate configuration against schema."""

        # Pydantic model validation
        try:
            ConfigModel(**config)
        except ValidationError as e:
            raise ConfigurationError(f"Invalid configuration: {e}")