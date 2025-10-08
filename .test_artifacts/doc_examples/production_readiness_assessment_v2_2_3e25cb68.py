# Example from: docs\production\production_readiness_assessment_v2.md
# Index: 2
# Runnable: True
# Hash: 3e25cb68

# Emergency Reset Conditions
emergency_reset = (
    not np.isfinite(u_sat) or abs(u_sat) > self.max_force * 2 or
    not np.isfinite(k1_new) or k1_new > self.k1_max * 0.9 or
    not np.isfinite(k2_new) or k2_new > self.k2_max * 0.9 or
    state_norm > 10.0 or velocity_norm > 50.0
)