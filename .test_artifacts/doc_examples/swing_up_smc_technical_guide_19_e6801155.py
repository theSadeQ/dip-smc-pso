# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 19
# Runnable: False
# Hash: e6801155

# example-metadata:
# runnable: false

# Aggressive finite-time convergence
stabilizer = SuperTwistingSMC(
    gains=[25, 10, 15, 12, 20, 15],  # [K1, K2, k1, k2, λ1, λ2]
    max_force=max_force
)

swing_up = SwingUpSMC(
    dynamics_model=dynamics,
    stabilizing_controller=stabilizer,
    energy_gain=60.0,
    switch_angle_tolerance=0.30  # Tighter (STA robust)
)