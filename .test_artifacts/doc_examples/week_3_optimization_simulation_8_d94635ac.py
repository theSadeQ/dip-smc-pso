# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 8
# Runnable: True
# Hash: d94635ac

def compute_chattering_index(control_signal, dt):
    """Total variation of control signal."""
    control_derivative = np.diff(control_signal) / dt
    return np.sum(np.abs(control_derivative)) * dt