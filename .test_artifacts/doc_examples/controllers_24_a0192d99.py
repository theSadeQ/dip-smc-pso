# Example from: docs\guides\api\controllers.md
# Index: 24
# Runnable: True
# Hash: a0192d99

# Classical with larger boundary layer
controller = create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 10])  # ε=10

# Or switch to STA for inherently smooth control
controller = create_smc_for_pso(SMCType.SUPER_TWISTING, [25, 10, 15, 12, 20, 15], dt=0.01)