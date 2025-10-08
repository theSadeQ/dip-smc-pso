# Example from: docs\mathematical_foundations\numerical_integration_theory.md
# Index: 2
# Runnable: False
# Hash: 1b9abbfe

def rk4_step(x, u, dynamics, dt):
    """Single RK4 integration step.

    Args:
        x: Current state (6,)
        u: Control input (scalar or function of time/state)
        dynamics: Dynamics model
        dt: Timestep

    Returns:
        x_next: State at t + dt
    """
    # Evaluate control at different stages if time-varying
    if callable(u):
        u1 = u(x)
        u2 = u(x + 0.5 * dt * k1)
        u3 = u(x + 0.5 * dt * k2)
        u4 = u(x + dt * k3)
    else:
        u1 = u2 = u3 = u4 = u  # Constant control

    # Four slope evaluations
    k1 = dynamics.compute_derivative(x, u1)
    k2 = dynamics.compute_derivative(x + 0.5 * dt * k1, u2)
    k3 = dynamics.compute_derivative(x + 0.5 * dt * k2, u3)
    k4 = dynamics.compute_derivative(x + dt * k3, u4)

    # Weighted combination
    x_next = x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    return x_next