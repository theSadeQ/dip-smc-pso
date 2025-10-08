# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 6
# Runnable: False
# Hash: e3a0d0c2

def compute_control(self, state, state_vars, history):
    """Main adaptive SMC control computation."""

    # 1. Unpack previous state
    prev_K, last_u, time_in_sliding = state_vars

    # 2. Extract state variables
    x, theta1, theta2, x_dot, theta1_dot, theta2_dot = state

    # 3. Compute sliding surface
    sigma = (self.k1 * (theta1_dot + self.lam1 * theta1) +
             self.k2 * (theta2_dot + self.lam2 * theta2))

    # 4. Switching term with current gain
    if self.smooth_switch:
        switching = saturate(sigma, self.boundary_layer, method="tanh")
    else:
        switching = saturate(sigma, self.boundary_layer, method="linear")

    u_sw = -prev_K * switching

    # 5. Total control with proportional term
    u = u_sw - self.alpha * sigma

    # 6. Actuator saturation
    u = np.clip(u, -self.max_force, self.max_force)

    # 7. Update time in sliding mode
    if abs(sigma) <= self.boundary_layer:
        new_time_in_sliding = time_in_sliding + self.dt
    else:
        new_time_in_sliding = 0.0

    # 8. Adaptive gain update
    if abs(sigma) <= self.dead_zone:
        dK = 0.0
    else:
        growth = self.gamma * abs(sigma)
        dK = growth - self.leak_rate * (prev_K - self.K_init)

    dK = np.clip(dK, -self.adapt_rate_limit, self.adapt_rate_limit)
    new_K = np.clip(prev_K + dK * self.dt, self.K_min, self.K_max)

    # 9. Update history
    hist = history
    hist.setdefault('K', []).append(new_K)
    hist.setdefault('sigma', []).append(sigma)
    hist.setdefault('u_sw', []).append(u_sw)
    hist.setdefault('dK', []).append(dK)
    hist.setdefault('time_in_sliding', []).append(new_time_in_sliding)

    # 10. Return structured output
    return AdaptiveSMCOutput(u, (new_K, u, new_time_in_sliding), hist, sigma)