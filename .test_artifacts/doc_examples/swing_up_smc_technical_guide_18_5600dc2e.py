# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 18
# Runnable: False
# Hash: 5600dc2e

# Conservative gains for handoff robustness
stabilizer = ClassicalSMC(
    gains=[8, 8, 12, 12, 40, 3],  # [k1, k2, λ1, λ2, K, kd]
    boundary_layer=0.02,          # Smooth handoff
    max_force=max_force
)

swing_up = SwingUpSMC(
    dynamics_model=dynamics,
    stabilizing_controller=stabilizer,
    energy_gain=50.0
)