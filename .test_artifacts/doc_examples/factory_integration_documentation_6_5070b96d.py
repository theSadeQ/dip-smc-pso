# Example from: docs\factory_integration_documentation.md
# Index: 6
# Runnable: False
# Hash: 5070b96d

def create_smc_for_pso(
    smc_type: SMCType,
    gains: Union[list, np.ndarray],
    plant_config_or_model: Optional[Any] = None,
    **kwargs: Any
) -> Any:
    """Create SMC controller optimized for PSO usage."""

def create_pso_controller_factory(
    smc_type: SMCType,
    plant_config: Optional[Any] = None,
    **kwargs: Any
) -> Callable:
    """Create a PSO-optimized controller factory function."""