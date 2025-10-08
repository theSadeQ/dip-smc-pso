# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 7
# Runnable: False
# Hash: ede536d0

# example-metadata:
# runnable: false

def compute_control(self, state: np.ndarray,
                   state_vars: tuple,
                   history: dict) -> ClassicalSMCOutput:
    """Main control computation."""
    # 1. Sliding surface
    sigma = self._compute_sliding_surface(state)

    # 2. Adaptive boundary layer
    eps_dyn = self.epsilon0 + self.epsilon1 * float(np.linalg.norm(sigma))

    # 3. Hysteresis dead-band
    if abs(float(sigma)) < self.hysteresis_ratio * self.epsilon0:
        sat_sigma = 0.0
    else:
        sat_sigma = saturate(sigma, eps_dyn, method=self.switch_method)

    # 4. Equivalent control
    u_eq = self._compute_equivalent_control(state)

    # 5. Clamp equivalent control
    max_eq = 5.0 * self.max_force
    u_eq = float(np.clip(u_eq, -max_eq, max_eq))

    # 6. Robust switching term
    u_robust = -self.K * sat_sigma - self.kd * sigma

    # 7. Combine and saturate
    u = u_eq + u_robust
    u_saturated = float(np.clip(u, -self.max_force, self.max_force))

    # 8. History tracking
    hist = history if isinstance(history, dict) else {}
    hist.setdefault('sigma', []).append(float(sigma))
    hist.setdefault('epsilon_eff', []).append(float(eps_dyn))
    hist.setdefault('u_eq', []).append(float(u_eq))
    hist.setdefault('u_robust', []).append(float(u_robust))
    hist.setdefault('u_total', []).append(float(u))
    hist.setdefault('u', []).append(float(u_saturated))

    return ClassicalSMCOutput(u_saturated, (), hist)