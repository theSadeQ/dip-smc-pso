# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 9
# Runnable: True
# Hash: 44ebd9a4

def compute_control_effort(control_signal, dt):
    """L2 norm of control signal."""
    return np.trapz(control_signal**2, dx=dt)