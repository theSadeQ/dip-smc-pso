# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 18
# Runnable: True
# Hash: a6a0996b

def load_factory_configuration(config_path: str) -> FactoryConfig:
    """
    Load and validate factory configuration from YAML.

    Performs comprehensive validation:
    - Mathematical constraint checking
    - PSO bounds validation
    - Controller parameter verification
    - Integration settings validation

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Validated FactoryConfig object

    Raises:
        ConfigurationError: If validation fails
    """
    import yaml
    from pydantic import ValidationError

    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)

    try:
        # Validate using Pydantic model
        factory_config = FactoryConfig(**config_dict)

        # Additional mathematical validation
        validate_mathematical_constraints(factory_config)

        return factory_config

    except ValidationError as e:
        raise ConfigurationError(f"Configuration validation failed: {e}")

@dataclass
class FactoryConfig:
    """Type-safe factory configuration."""
    controllers: Dict[str, ControllerConfig]
    pso: PSOConfig
    factory: FactorySettings

    def __post_init__(self):
        """Validate configuration after loading."""
        # Ensure all required controllers are configured
        required_controllers = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']
        for controller_type in required_controllers:
            if controller_type not in self.controllers:
                raise ValueError(f"Missing configuration for {controller_type}")

        # Validate PSO bounds consistency
        self._validate_pso_bounds()

    def _validate_pso_bounds(self):
        """Validate PSO bounds against mathematical constraints."""
        for controller_type, bounds in self.pso.bounds.items():
            if controller_type == 'sta_smc':
                # Ensure K1 bounds > K2 bounds for STA-SMC
                k1_bounds = bounds.get('K1', [2.0, 100.0])
                k2_bounds = bounds.get('K2', [1.0, 99.0])
                if k1_bounds[0] <= k2_bounds[1]:
                    raise ValueError("STA-SMC bounds must ensure K1 > K2")