# Example from: docs\controllers\mpc_technical_guide.md
# Index: 8
# Runnable: True
# Hash: b5f8b687

def ref_fn(t):
    """Time-varying reference trajectory."""
    x_target = 0.5 * sin(0.5*π*t)  # Sinusoidal cart motion
    return np.array([x_target, π, π, 0, 0, 0])

mpc.set_reference(ref_fn)