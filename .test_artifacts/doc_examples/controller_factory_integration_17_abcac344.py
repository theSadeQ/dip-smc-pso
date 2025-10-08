# Example from: docs\technical\controller_factory_integration.md
# Index: 17
# Runnable: False
# Hash: abcac344

# example-metadata:
# runnable: false

def create_pso_controller_factory(
    smc_type: SMCType,
    plant_config: Optional[Any] = None,
    max_force: float = 150.0,
    dt: float = 0.001,
    **kwargs
) -> Callable:
    """Create a PSO-optimized controller factory function."""

    def controller_factory(gains: Union[list, np.ndarray]) -> Any:
        """Controller factory function optimized for PSO."""
        return create_smc_for_pso(smc_type, gains, plant_config, max_force, dt, **kwargs)

    # Add PSO-required attributes
    controller_factory.n_gains = get_expected_gain_count(smc_type)
    controller_factory.controller_type = smc_type.value

    return controller_factory