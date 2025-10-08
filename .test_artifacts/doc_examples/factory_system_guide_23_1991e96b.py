# Example from: docs\controllers\factory_system_guide.md
# Index: 23
# Runnable: False
# Hash: 1991e96b

# Clean SMC Factory
controller = SMCFactory.create_from_gains(
    smc_type=SMCType.SUPER_TWISTING,
    gains=[25.0, 15.0, 20.0, 12.0, 8.0, 6.0],  # [K1, K2, k1, k2, λ1, λ2]
    max_force=100.0,
    dt=0.01,
    damping_gain=0.0,
    boundary_layer=0.01,
    dynamics_model=dynamics_model
)

# Constraint validation (K1 > K2)
K1, K2 = gains[0], gains[1]
if K1 <= K2:
    raise ValueError("Super-Twisting stability requires K1 > K2 > 0")