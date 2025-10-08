# Example from: docs\controllers\factory_system_guide.md
# Index: 15
# Runnable: False
# Hash: 19582273

# example-metadata:
# runnable: false

def create_pso_controller_factory(smc_type: SMCType, **kwargs) -> Callable:
    """Create a PSO-optimized controller factory function."""

    def controller_factory(gains: Union[list, np.ndarray]) -> Any:
        return create_smc_for_pso(smc_type, gains, **kwargs)

    # Add PSO-required attributes
    spec = SMC_GAIN_SPECS[smc_type]
    controller_factory.n_gains = spec.n_gains
    controller_factory.controller_type = smc_type.value
    controller_factory.max_force = kwargs.get('max_force', 150.0)

    return controller_factory