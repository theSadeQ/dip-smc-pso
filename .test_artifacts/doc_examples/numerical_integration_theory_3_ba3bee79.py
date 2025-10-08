# Example from: docs\mathematical_foundations\numerical_integration_theory.md
# Index: 3
# Runnable: False
# Hash: ba3bee79

# example-metadata:
# runnable: false

def rk45_adaptive_step(x, u, dynamics, t, dt, tol=1e-6):
    """Adaptive RK45 step with error control.

    Args:
        x: Current state (6,)
        u: Control input
        dynamics: Dynamics model
        t: Current time
        dt: Suggested timestep
        tol: Error tolerance

    Returns:
        x_next: Accepted state
        dt_next: Suggested next timestep
        error: Estimated error
    """
    # Dormand-Prince coefficients
    a21 = 1/5
    a31, a32 = 3/40, 9/40
    a41, a42, a43 = 44/45, -56/15, 32/9
    a51, a52, a53, a54 = 19372/6561, -25360/2187, 64448/6561, -212/729
    a61, a62, a63, a64, a65 = 9017/3168, -355/33, 46732/5247, 49/176, -5103/18656

    # 4th order solution weights
    b1, b3, b4, b5, b6 = 35/384, 500/1113, 125/192, -2187/6784, 11/84

    # 5th order solution weights (for error estimate)
    b1_star = 5179/57600
    b3_star = 7571/16695
    b4_star = 393/640
    b5_star = -92097/339200
    b6_star = 187/2100
    b7_star = 1/40

    # Six slope evaluations
    k1 = dynamics.compute_derivative(x, u)
    k2 = dynamics.compute_derivative(x + dt*a21*k1, u)
    k3 = dynamics.compute_derivative(x + dt*(a31*k1 + a32*k2), u)
    k4 = dynamics.compute_derivative(x + dt*(a41*k1 + a42*k2 + a43*k3), u)
    k5 = dynamics.compute_derivative(x + dt*(a51*k1 + a52*k2 + a53*k3 + a54*k4), u)
    k6 = dynamics.compute_derivative(x + dt*(a61*k1 + a62*k2 + a63*k3 + a64*k4 + a65*k5), u)

    # 4th order solution
    x4 = x + dt * (b1*k1 + b3*k3 + b4*k4 + b5*k5 + b6*k6)

    # 5th order solution
    k7 = dynamics.compute_derivative(x4, u)  # FSAL property
    x5 = x + dt * (b1_star*k1 + b3_star*k3 + b4_star*k4 + b5_star*k5 + b6_star*k6 + b7_star*k7)

    # Error estimate
    error = np.linalg.norm(x5 - x4) / (tol + tol * np.linalg.norm(x))

    # Timestep adaptation
    if error < 1.0:
        # Accept step
        dt_next = dt * min(5.0, max(0.2, 0.9 * (1.0 / error)**(1/5)))
        return x4, dt_next, error
    else:
        # Reject step, retry with smaller dt
        dt_new = dt * max(0.2, 0.9 * (1.0 / error)**(1/5))
        return rk45_adaptive_step(x, u, dynamics, t, dt_new, tol)