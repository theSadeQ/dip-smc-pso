# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 24
# Runnable: True
# Hash: 521c6e46

# Modern type-safe factory usage
from controllers import SMCFactory, SMCConfig, SMCType

# Type-safe configuration
config = SMCConfig(
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0,
    dt=0.01,
    boundary_layer=0.01
)

# Create controller with full validation
controller = SMCFactory.create_controller(SMCType.CLASSICAL, config)

# PSO integration
optimized_controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    optimized_gains,
    max_force=100.0
)