# Example from: docs\controllers\mpc_technical_guide.md
# Index: 16
# Runnable: True
# Hash: 32abf21d

# Custom SMC fallback
mpc = MPCController(
    dynamics,
    fallback_smc_gains=[10, 8, 15, 12, 50, 5],  # [k1,k2,λ1,λ2,K,kd]
    fallback_boundary_layer=0.01
)