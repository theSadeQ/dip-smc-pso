# Example from: docs\guides\workflows\hil-workflow.md
# Index: 2
# Runnable: True
# Hash: a393191d

import numpy as np
import matplotlib.pyplot as plt

# Load HIL results
data = np.load('out/hil_results.npz', allow_pickle=True)

print("Metadata:", data['meta'].item())
print("Duration:", data['t'][-1], "seconds")
print("Steps:", len(data['t']))

# Extract data
t = data['t']         # Time vector (1001,)
x = data['x']         # State trajectory (1001, 6)
u = data['u']         # Control signal (1000,)

# Plot state trajectory
fig, axes = plt.subplots(3, 1, figsize=(10, 8))

axes[0].plot(t, x[:, 0])
axes[0].set_ylabel('Cart Position (m)')
axes[0].grid(True)

axes[1].plot(t, x[:, 1], label='Pendulum 1')
axes[1].plot(t, x[:, 2], label='Pendulum 2')
axes[1].set_ylabel('Angle (rad)')
axes[1].legend()
axes[1].grid(True)

axes[2].plot(t[:-1], u)
axes[2].set_ylabel('Control Force (N)')
axes[2].set_xlabel('Time (s)')
axes[2].grid(True)

plt.tight_layout()
plt.savefig('hil_results.png', dpi=150)
plt.show()