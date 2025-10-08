# Example from: docs\factory\factory_api_reference.md
# Index: 17
# Runnable: True
# Hash: d408b379

def create_pso_controller_factory(
    smc_type: SMCType,
    plant_config: Optional[Any] = None,
    **kwargs: Any
) -> Callable[[Union[List[float], np.ndarray]], Any]