# Example from: docs\api\factory_system_api_reference.md
# Index: 31
# Runnable: False
# Hash: a36aff8a

def create_pso_controller_factory(
    smc_type: SMCType,
    plant_config: Optional[Any] = None,
    **kwargs: Any
) -> Callable:
    """Create a PSO-optimized controller factory function with required attributes.

    Returns:
        Factory function with attributes:
        - n_gains: Expected gain count
        - controller_type: Controller type string
        - max_force: Maximum control force
    """
    def controller_factory(gains: Union[list, np.ndarray]) -> Any:
        return create_smc_for_pso(smc_type, gains, plant_config, **kwargs)

    # Add PSO-required attributes
    controller_factory.n_gains = get_expected_gain_count(smc_type)
    controller_factory.controller_type = smc_type.value
    controller_factory.max_force = kwargs.get('max_force', 150.0)

    return controller_factory