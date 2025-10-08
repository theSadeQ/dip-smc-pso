# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 5
# Runnable: False
# Hash: 2515d9ed

# example-metadata:
# runnable: false

# Added emergency reset conditions
emergency_reset = (
    not np.isfinite(u_sat) or abs(u_sat) > self.max_force * 2 or
    not np.isfinite(k1_new) or k1_new > self.k1_max * 0.9 or
    not np.isfinite(k2_new) or k2_new > self.k2_max * 0.9 or
    not np.isfinite(u_int_new) or abs(u_int_new) > self.u_int_max * 1.5 or
    not np.isfinite(s) or abs(s) > 100.0 or
    state_norm > 10.0 or velocity_norm > 50.0
)

if emergency_reset:
    # Safe fallback values
    u_sat = 0.0
    k1_new = max(0.0, min(self.k1_init * 0.05, self.k1_max * 0.05))
    k2_new = max(0.0, min(self.k2_init * 0.05, self.k2_max * 0.05))
    u_int_new = 0.0