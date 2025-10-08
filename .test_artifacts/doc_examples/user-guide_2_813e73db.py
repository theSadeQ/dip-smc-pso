# Example from: docs\guides\user-guide.md
# Index: 2
# Runnable: True
# Hash: 813e73db

import json
import numpy as np
import matplotlib.pyplot as plt

# Load saved results
data = json.load(open('results_classical.json'))

# Extract time series
t = np.array(data['time'])
x = np.array(data['state'])
u = np.array(data['control'])

# Access specific states
cart_pos = x[:, 0]          # Cart position
cart_vel = x[:, 1]          # Cart velocity
theta1 = x[:, 2]            # First pendulum angle
theta1_dot = x[:, 3]        # First pendulum velocity
theta2 = x[:, 4]            # Second pendulum angle
theta2_dot = x[:, 5]        # Second pendulum velocity

# Access performance metrics
print(f"ISE: {data['metrics']['ise']:.4f}")
print(f"Settling Time: {data['metrics']['settling_time']:.2f} s")
print(f"Peak Overshoot: {data['metrics']['overshoot']:.2f}%")

# Custom analysis: Compute energy
def compute_energy(x, m0=1.0, m1=0.1, m2=0.1, l1=0.5, l2=0.5, g=9.81):
    """Compute total system energy."""
    cart_pos, cart_vel, theta1, theta1_dot, theta2, theta2_dot = x.T

    # Kinetic energy
    KE_cart = 0.5 * m0 * cart_vel**2
    KE_p1 = 0.5 * m1 * (cart_vel**2 + l1**2 * theta1_dot**2)
    KE_p2 = 0.5 * m2 * (cart_vel**2 + l1**2 * theta1_dot**2 + l2**2 * theta2_dot**2)

    # Potential energy (relative to equilibrium)
    PE_p1 = m1 * g * l1 * (1 - np.cos(theta1))
    PE_p2 = m2 * g * (l1 * (1 - np.cos(theta1)) + l2 * (1 - np.cos(theta2)))

    return KE_cart + KE_p1 + KE_p2 + PE_p1 + PE_p2

energy = compute_energy(x)

# Plot energy dissipation
plt.figure()
plt.plot(t, energy)
plt.xlabel('Time (s)')
plt.ylabel('Total Energy (J)')
plt.title('Energy Dissipation via Control')
plt.grid()
plt.show()