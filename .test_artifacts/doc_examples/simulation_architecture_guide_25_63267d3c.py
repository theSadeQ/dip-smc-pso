# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 25
# Runnable: False
# Hash: 63267d3c

# Wrap simulation in try-except for safety guard violations
try:
    states = simulate(x0, u, dt, energy_limits=100.0)
    success = True
except ValueError as e:
    # Safety guard triggered
    print(f"Simulation failed: {e}")
    success = False

# Use early stopping instead of throwing errors
def soft_stop(state):
    """Return True when unstable, but don't raise error."""
    return abs(state[1]) > np.pi/2 or np.sum(state**2) > 100.0

states = simulate(x0, u, dt, stop_fn=soft_stop)
# states.shape[0] may be < horizon + 1