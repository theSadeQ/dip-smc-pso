# Example from: docs\controllers\factory_system_guide.md
# Index: 13
# Runnable: False
# Hash: 96352dc3

# Direct from gains array
controller = SMCFactory.create_from_gains(
    smc_type=SMCType.CLASSICAL,
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0,
    dt=0.01
)

# From full configuration
config = SMCConfig(
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0,
    dt=0.01,
    boundary_layer=0.02
)
controller = SMCFactory.create_controller(SMCType.CLASSICAL, config)