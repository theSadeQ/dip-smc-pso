# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 12
# Runnable: True
# Hash: 23576859

from src.controllers.factory import SMCFactory, SMCConfig

# Create configuration dataclass
config = SMCConfig(
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 0.01],
    max_force=100.0,
    dt=0.01,
    boundary_layer=0.01
)

# Factory ensures type safety
controller = SMCFactory.create_controller(SMCType.CLASSICAL, config)

# mypy validates this at compile time!