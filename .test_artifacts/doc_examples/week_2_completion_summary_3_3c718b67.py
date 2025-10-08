# Example from: docs\plans\documentation\week_2_completion_summary.md
# Index: 3
# Runnable: False
# Hash: 3c718b67

# Enterprise Factory
controller = create_controller('classical_smc', config, gains=[...])

# Clean SMC Factory
controller = SMCFactory.create_from_gains(
    SMCType.CLASSICAL,
    gains=[...],
    max_force=100.0
)

# PSO Integration
controller = create_smc_for_pso(SMCType.CLASSICAL, gains_array)