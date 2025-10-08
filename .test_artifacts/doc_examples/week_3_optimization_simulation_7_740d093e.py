# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 7
# Runnable: True
# Hash: 740d093e

def compute_ise(states):
    """Integral of Squared Error."""
    return np.trapz(states**2, dx=dt)

def compute_itae(time, states):
    """Integral of Time-weighted Absolute Error."""
    return np.trapz(time * np.abs(states), dx=dt)