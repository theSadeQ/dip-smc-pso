# Example from: docs\api\factory_methods_reference.md
# Index: 16
# Runnable: True
# Hash: e584e1b8

def create_pso_controller_factory(
    smc_type: SMCType,
    plant_config: Optional[Any] = None,
    **kwargs: Any
) -> Callable[[Union[list, np.ndarray]], PSOControllerWrapper]