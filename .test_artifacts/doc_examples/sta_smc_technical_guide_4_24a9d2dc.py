# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 4
# Runnable: False
# Hash: 24a9d2dc

# example-metadata:
# runnable: false

def compute_control(self, state, state_vars, history):
    """Compute STA-SMC control with Numba acceleration."""

    # Unpack integrator state
    try:
        z, _ = state_vars  # Ignore provided sigma, will recompute
    except:
        z = float(state_vars) if state_vars is not None else 0.0

    # Equivalent control (model-based, optional)
    u_eq = self._compute_equivalent_control(state)

    # Sliding surface
    sigma = self._compute_sliding_surface(state)

    # Saturated sign function
    sgn_sigma = saturate(sigma, self.boundary_layer, method=self.switch_method)

    # Call Numba-accelerated core
    u, new_z, sigma_val = _sta_smc_core(
        z=z,
        sigma=float(sigma),
        sgn_sigma=float(sgn_sigma),
        alg_gain_K1=self.alg_gain_K1,
        alg_gain_K2=self.alg_gain_K2,
        damping_gain=self.damping_gain,
        dt=self.dt,
        max_force=self.max_force,
        u_eq=u_eq,
        Kaw=self.anti_windup_gain
    )

    # Update history
    hist = history if isinstance(history, dict) else {}
    hist.setdefault('sigma', []).append(float(sigma))
    hist.setdefault('z', []).append(float(new_z))
    hist.setdefault('u', []).append(float(u))
    hist.setdefault('u_eq', []).append(float(u_eq))

    return STAOutput(u, (new_z, float(sigma)), hist)