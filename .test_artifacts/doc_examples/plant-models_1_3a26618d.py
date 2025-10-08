# Example from: docs\guides\api\plant-models.md
# Index: 1
# Runnable: True
# Hash: 3a26618d

state = np.array([
    x,        # Cart position (m)
    dx,       # Cart velocity (m/s)
    theta1,   # First pendulum angle (rad, 0 = upright)
    dtheta1,  # First pendulum angular velocity (rad/s)
    theta2,   # Second pendulum angle (rad, 0 = upright)
    dtheta2   # Second pendulum angular velocity (rad/s)
])