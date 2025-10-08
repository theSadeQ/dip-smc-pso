# Example from: docs\controllers\mpc_technical_guide.md
# Index: 21
# Runnable: True
# Hash: 7f1eb000

mpc = MPCController(
    dynamics_model=dynamics,
    horizon=20,
    dt=0.02,
    max_theta_dev=0.3,              # Tighter angle bounds
    fallback_smc_gains=[8, 8, 12, 12, 40, 3],
    fallback_boundary_layer=0.02
)