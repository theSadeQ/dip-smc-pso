# Example from: docs\factory\pso_factory_api_reference.md
# Index: 13
# Runnable: False
# Hash: 71adf638

@dataclass(frozen=True)
class PSOFactoryConfig:
    """
    Complete configuration for PSO-Factory integration.

    Provides type-safe configuration with automatic validation
    and mathematical constraint checking.
    """

    # Controller configuration
    controller_type: SMCType
    max_force: float = 100.0
    dt: float = 0.01

    # PSO algorithm parameters
    pso_params: Dict[str, Any] = field(default_factory=lambda: {
        'n_particles': 30,
        'iters': 100,
        'c1': 2.0,
        'c2': 2.0,
        'w': 0.9
    })

    # Performance monitoring
    enable_monitoring: bool = True
    enable_caching: bool = True
    cache_size: int = 1000

    # Validation settings
    strict_validation: bool = True
    constraint_tolerance: float = 1e-8

    # PSO bounds (auto-derived if None)
    custom_bounds: Optional[List[Tuple[float, float]]] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.max_force <= 0:
            raise ValueError("max_force must be positive")
        if self.dt <= 0:
            raise ValueError("dt must be positive")
        if not isinstance(self.controller_type, SMCType):
            raise TypeError("controller_type must be SMCType")

        # Validate PSO parameters
        if self.pso_params['n_particles'] < 10:
            raise ValueError("n_particles should be ≥ 10")
        if self.pso_params['iters'] < 10:
            raise ValueError("iters should be ≥ 10")

    @property
    def gain_bounds(self) -> List[Tuple[float, float]]:
        """Get PSO bounds (custom or auto-derived)."""
        if self.custom_bounds is not None:
            return self.custom_bounds
        return get_gain_bounds_for_pso(self.controller_type)

    @property
    def n_gains(self) -> int:
        """Get number of gain parameters."""
        return self.controller_type.gain_count

def load_factory_config(config_dict: Dict[str, Any]) -> PSOFactoryConfig:
    """
    Load and validate factory configuration from dictionary.

    Args:
        config_dict: Configuration dictionary

    Returns:
        Validated PSOFactoryConfig object

    Raises:
        ConfigurationError: If validation fails
    """
    try:
        # Convert string controller type to enum
        if isinstance(config_dict.get('controller_type'), str):
            config_dict['controller_type'] = SMCType(config_dict['controller_type'])

        return PSOFactoryConfig(**config_dict)
    except (ValueError, TypeError) as e:
        raise ConfigurationError(f"Invalid factory configuration: {e}")