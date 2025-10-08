# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 2
# Runnable: True
# Hash: 0e3c12cb

emergency_reset = (
    not np.isfinite(u_sat) or abs(u_sat) > max_force * 2 or
    not np.isfinite(k1_new) or k1_new > k1_max * 0.9 or
    not np.isfinite(k2_new) or k2_new > k2_max * 0.9 or
    state_norm > 10.0 or velocity_norm > 50.0
)