# Example from: docs\controllers\factory_system_guide.md
# Index: 5
# Runnable: False
# Hash: a69c691e

# example-metadata:
# runnable: false

# Method 1: String-based creation
controller = create_controller(
    controller_type='classical_smc',
    config=config,
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
)

# Method 2: Enum-based creation (type-safe)
controller = SMCFactory.create_controller(
    smc_type=SMCType.CLASSICAL,
    config=SMCConfig(gains=[10, 8, 15, 12, 50, 5], max_force=100, dt=0.01)
)

# Method 3: Backwards-compatible aliases
controller = create_classical_smc_controller(config, gains=[...])