# Example from: docs\guides\api\controllers.md
# Index: 25
# Runnable: True
# Hash: 5fc8ee15

# Must specify dt for STA and Hybrid controllers
controller = create_smc_for_pso(SMCType.SUPER_TWISTING, gains, dt=0.01)
controller = create_smc_for_pso(SMCType.HYBRID, gains, dt=0.01)