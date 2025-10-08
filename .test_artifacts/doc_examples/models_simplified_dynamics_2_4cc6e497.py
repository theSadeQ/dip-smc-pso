# Example from: docs\reference\plant\models_simplified_dynamics.md
# Index: 2
# Runnable: True
# Hash: 4cc6e497

import numpy as np
import matplotlib.pyplot as plt

# Simulate and track energy
dynamics = SimplifiedDynamics()
states = [initial_state]
energies = []

for t in np.arange(0, 10, 0.01):
    state = states[-1]
    u = controller.compute_control(state, t)

    # Compute energy before step
    E = dynamics.compute_total_energy(state)
    energies.append(E)

    # Integrate
    x_dot = dynamics.compute_dynamics(state, u, t)
    next_state = state + 0.01 * x_dot
    states.append(next_state)

# Plot energy conservation
plt.plot(energies)
plt.xlabel('Time step')
plt.ylabel('Total Energy (J)')
plt.title('Energy Conservation Analysis')
plt.grid(True)
plt.show()

energy_drift = abs(energies[-1] - energies[0]) / energies[0] * 100
print(f"Energy drift: {energy_drift:.2f}%")