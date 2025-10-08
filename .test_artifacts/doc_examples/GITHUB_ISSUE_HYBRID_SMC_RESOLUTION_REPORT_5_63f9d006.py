# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 5
# Runnable: False
# Hash: 63f9d006

def _check_emergency_conditions(self, u_sat, k1_new, k2_new, u_int_new, s, state):
    """Check for numerical instability requiring emergency reset."""
    state_norm = np.linalg.norm(state[:3])  # Position magnitudes
    velocity_norm = np.linalg.norm(state[3:])  # Velocity magnitudes

    emergency_reset = (
        not np.isfinite(u_sat) or abs(u_sat) > self.max_force * 2 or
        not np.isfinite(k1_new) or k1_new > self.k1_max * 0.9 or
        not np.isfinite(k2_new) or k2_new > self.k2_max * 0.9 or
        not np.isfinite(u_int_new) or abs(u_int_new) > self.u_int_max * 1.5 or
        not np.isfinite(s) or abs(s) > 100.0 or
        state_norm > 10.0 or velocity_norm > 50.0
    )

    return emergency_reset