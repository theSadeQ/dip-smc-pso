# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 12
# Runnable: True
# Hash: 4aff105c

def create_smc_for_pso(
    smc_type: SMCType,
    gains: Union[List[float], np.ndarray],
    **kwargs: Any
) -> PSOControllerWrapper:
    """Create SMC controller with PSO-compatible interface."""