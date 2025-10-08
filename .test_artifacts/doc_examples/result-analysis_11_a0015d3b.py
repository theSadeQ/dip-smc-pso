# Example from: docs\guides\how-to\result-analysis.md
# Index: 11
# Runnable: True
# Hash: a0015d3b

import matplotlib.pyplot as plt

# Load data
with open('results_classical.json') as f:
    data = json.load(f)

time = np.array(data['time'])
state = np.array(data['state'])
control = np.array(data['control'])

# Create figure
fig, axes = plt.subplots(3, 1, figsize=(12, 9))

# Pendulum angles
axes[0].plot(time, state[:, 2], 'b-', linewidth=2, label='θ₁ (first pendulum)')
axes[0].plot(time, state[:, 4], 'r-', linewidth=2, label='θ₂ (second pendulum)')
axes[0].axhline(0, color='k', linestyle='--', linewidth=0.5)
axes[0].set_ylabel('Angle (rad)', fontsize=12)
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3)

# Angular velocities
axes[1].plot(time, state[:, 3], 'b-', linewidth=2, label='dθ₁')
axes[1].plot(time, state[:, 5], 'r-', linewidth=2, label='dθ₂')
axes[1].axhline(0, color='k', linestyle='--', linewidth=0.5)
axes[1].set_ylabel('Angular Velocity (rad/s)', fontsize=12)
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3)

# Control signal
axes[2].plot(time, control, 'g-', linewidth=2)
axes[2].axhline(100, color='r', linestyle='--', label='Max force')
axes[2].axhline(-100, color='r', linestyle='--')
axes[2].set_xlabel('Time (s)', fontsize=12)
axes[2].set_ylabel('Control Force (N)', fontsize=12)
axes[2].legend(fontsize=10)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('state_trajectories.png', dpi=300)
plt.savefig('state_trajectories.pdf')
plt.show()