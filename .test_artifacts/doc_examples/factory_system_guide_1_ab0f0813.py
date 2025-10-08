# Example from: docs\controllers\factory_system_guide.md
# Index: 1
# Runnable: False
# Hash: ab0f0813

# example-metadata:
# runnable: false

# Single Responsibility - Each factory focuses on specific concerns
Enterprise Factory: Comprehensive configuration, backwards compatibility
Clean SMC Factory: PSO optimization, research benchmarking

# Dependency Injection - Controllers receive dependencies at creation
controller = create_controller(
    'classical_smc',
    config=config,
    gains=[10, 8, 15, 12, 50, 5]
)

# Type Safety - Explicit typing for all interfaces
def create_controller(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[list, np.ndarray]] = None
) -> Any:
    ...