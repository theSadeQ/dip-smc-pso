# Example from: docs\guides\how-to\running-simulations.md
# Index: 3
# Runnable: True
# Hash: f001e8b2

from src.controllers import create_smc_for_pso, SMCType
from src.plant.models.dynamics import DoubleInvertedPendulum
import numpy as np

# Initialize system
dt = 0.01
duration = 5.0
steps = int(duration / dt)

# Create dynamics model
dynamics = DoubleInvertedPendulum(
    m0=1.0, m1=0.1, m2=0.1,
    l1=0.5, l2=0.5,
    g=9.81
)

# Create controller
controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)

# Initialize state
state = np.array([0.0, 0.0, 0.1, 0.0, 0.15, 0.0])
state_vars = {}
history = controller.initialize_history()

# Storage
time_log = []
state_log = []
control_log = []

# Simulation loop
for i in range(steps):
    # Compute control
    u, state_vars, history = controller.compute_control(
        state, state_vars, history
    )

    # Apply dynamics (using RK4 or Euler)
    state = dynamics.step(state, u, dt)  # Your integration method

    # Log data
    time_log.append(i * dt)
    state_log.append(state.copy())
    control_log.append(u)

# Convert to arrays
time_array = np.array(time_log)
state_array = np.array(state_log)
control_array = np.array(control_log)

print(f"Final state: {state_array[-1]}")