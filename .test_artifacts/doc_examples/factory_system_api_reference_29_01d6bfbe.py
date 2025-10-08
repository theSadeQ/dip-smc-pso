# Example from: docs\api\factory_system_api_reference.md
# Index: 29
# Runnable: False
# Hash: 01d6bfbe

def create_smc_for_pso(
    smc_type: SMCType,
    gains: Union[list, np.ndarray],
    plant_config_or_model: Optional[Any] = None,
    **kwargs: Any
) -> PSOControllerWrapper:
    """Create SMC controller optimized for PSO usage.

    Args:
        smc_type: Controller type (SMCType enum)
        gains: Gain vector from PSO particle
        plant_config_or_model: Plant configuration (optional)
        **kwargs: Additional parameters (max_force, dt, etc.)

    Returns:
        PSOControllerWrapper instance with PSO-compatible interface
    """