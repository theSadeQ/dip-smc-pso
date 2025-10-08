# Example from: docs\guides\how-to\result-analysis.md
# Index: 13
# Runnable: False
# Hash: 9b031965

# example-metadata:
# runnable: false

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# First pendulum phase portrait
axes[0].plot(state[:, 2], state[:, 3], 'b-', linewidth=1.5)
axes[0].plot(state[0, 2], state[0, 3], 'go', markersize=10, label='Start')
axes[0].plot(state[-1, 2], state[-1, 3], 'ro', markersize=10, label='End')
axes[0].set_xlabel('θ₁ (rad)', fontsize=12)
axes[0].set_ylabel('dθ₁ (rad/s)', fontsize=12)
axes[0].set_title('First Pendulum Phase Portrait', fontsize=14)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Second pendulum phase portrait
axes[1].plot(state[:, 4], state[:, 5], 'r-', linewidth=1.5)
axes[1].plot(state[0, 4], state[0, 5], 'go', markersize=10, label='Start')
axes[1].plot(state[-1, 4], state[-1, 5], 'ro', markersize=10, label='End')
axes[1].set_xlabel('θ₂ (rad)', fontsize=12)
axes[1].set_ylabel('dθ₂ (rad/s)', fontsize=12)
axes[1].set_title('Second Pendulum Phase Portrait', fontsize=14)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('phase_portraits.png', dpi=300)
plt.show()