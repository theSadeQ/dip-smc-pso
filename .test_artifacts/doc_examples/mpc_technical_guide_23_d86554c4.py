# Example from: docs\controllers\mpc_technical_guide.md
# Index: 23
# Runnable: False
# Hash: d86554c4

# Simulation loop
t = 0.0
dt = 0.02
x = np.array([0.0, np.pi, np.pi, 0.0, 0.0, 0.0])  # Upright

while t < 10.0:
    # Compute MPC control
    u = mpc.compute_control(t, x)

    # Apply to system
    x = dynamics.step(x, u, dt)

    # Advance time
    t += dt