# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 16
# Runnable: True
# Hash: 49a827b0

from src.simulation.context.safety_guards import _guard_no_nan

def custom_guard_angular_velocity(state, t, threshold=100.0):
    """Custom guard for excessive angular velocities."""
    theta1_dot = state[4]
    theta2_dot = state[5]

    if abs(theta1_dot) > threshold or abs(theta2_dot) > threshold:
        raise ValueError(
            f"Angular velocity limit exceeded at t={t:.3f}: "
            f"θ̇1={theta1_dot:.2f}, θ̇2={theta2_dot:.2f}"
        )

# Integrate custom guard into simulation loop
for i in range(horizon):
    x_next = step(x_current, u[i], dt)
    _guard_no_nan(x_next, t, dt)
    custom_guard_angular_velocity(x_next, t, threshold=50.0)
    x_current = x_next
    t += dt