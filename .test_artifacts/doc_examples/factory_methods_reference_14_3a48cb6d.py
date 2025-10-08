# Example from: docs\api\factory_methods_reference.md
# Index: 14
# Runnable: True
# Hash: 3a48cb6d

def create_smc_for_pso(
    smc_type: SMCType,
    gains: Union[list, np.ndarray],
    plant_config_or_model: Optional[Any] = None,
    **kwargs: Any
) -> PSOControllerWrapper