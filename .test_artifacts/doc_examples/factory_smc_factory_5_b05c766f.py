# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 5
# Runnable: False
# Hash: b05c766f

def create_controller(
    ctrl_type: SMCType,
    gains: List[float],
    dynamics_model: Optional[DynamicsModel] = None,  # Injected
    config: Optional[Config] = None  # Injected
) -> Controller:
    ...