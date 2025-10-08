# Example from: docs\controllers\mpc_technical_guide.md
# Index: 24
# Runnable: True
# Hash: 369444d7

def reference_trajectory(t):
    """Sinusoidal cart motion while keeping pendulum upright."""
    x_ref = 0.5 * np.sin(0.5 * np.pi * t)
    return np.array([x_ref, np.pi, np.pi, 0.0, 0.0, 0.0])

mpc.set_reference(reference_trajectory)

# Now MPC tracks this time-varying reference
u = mpc.compute_control(t=2.0, x0=x_current)