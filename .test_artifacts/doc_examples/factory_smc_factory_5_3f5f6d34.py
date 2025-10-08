# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 5
# Runnable: False
# Hash: 3f5f6d34

# example-metadata:
# runnable: false

def create_controller(
    ctrl_type: SMCType,
    gains: List[float],
    dynamics_model: Optional[DynamicsModel] = None,  # Injected
    config: Optional[Config] = None  # Injected
) -> Controller:
    ...