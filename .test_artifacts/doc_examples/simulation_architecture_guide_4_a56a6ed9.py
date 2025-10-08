# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 4
# Runnable: True
# Hash: a56a6ed9

# Stop when pendulum falls (|θ1| > π/2)
def stop_condition(state):
    return abs(state[1]) > np.pi / 2

x0 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
u = np.random.randn(1000) * 0.1  # Large disturbance

states = simulate(x0, u, dt, stop_fn=stop_condition)

print(f"Simulation stopped at step {len(states)-1}")  # May be < 1000