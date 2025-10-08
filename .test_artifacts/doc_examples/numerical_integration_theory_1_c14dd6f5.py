# Example from: docs\mathematical_foundations\numerical_integration_theory.md
# Index: 1
# Runnable: False
# Hash: c14dd6f5

# example-metadata:
# runnable: false

def euler_step(x, u, dynamics, dt):
    """Single Euler integration step.

    Args:
        x: Current state (6,)
        u: Control input (scalar)
        dynamics: Dynamics model
        dt: Timestep

    Returns:
        x_next: State at t + dt
    """
    dxdt = dynamics.compute_derivative(x, u)
    x_next = x + dt * dxdt
    return x_next