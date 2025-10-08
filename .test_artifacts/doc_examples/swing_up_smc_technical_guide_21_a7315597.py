# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 21
# Runnable: False
# Hash: a7315597

# example-metadata:
# runnable: false

# Initial state: down-down (fully inverted)
x = np.array([0.0, np.pi, np.pi, 0.0, 0.0, 0.0])

# Initialize controller state
state_vars = swing_up.initialize_state()
history = swing_up.initialize_history()

# Simulation loop
t = 0.0
dt = 0.01
u_history = []
mode_history = []

while t < 10.0:
    # Compute control
    u, state_vars, history = swing_up.compute_control(x, state_vars, history)

    # Log telemetry
    u_history.append(u)
    mode_history.append(history["mode"])

    # Apply to system
    x = dynamics.step(x, u, dt)

    # Advance time
    t += dt

# Analyze handoff time
if swing_up.switch_time is not None:
    print(f"Handoff occurred at t = {swing_up.switch_time:.3f} s")