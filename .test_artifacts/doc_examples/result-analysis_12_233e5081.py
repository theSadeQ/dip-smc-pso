# Example from: docs\guides\how-to\result-analysis.md
# Index: 12
# Runnable: False
# Hash: 233e5081

# example-metadata:
# runnable: false

controllers = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']
colors = ['blue', 'red', 'green', 'purple']
labels = ['Classical', 'Super-Twisting', 'Adaptive', 'Hybrid']

fig, ax = plt.subplots(figsize=(12, 6))

for ctrl, color, label in zip(controllers, colors, labels):
    with open(f'results_{ctrl}.json') as f:
        data = json.load(f)

    time = np.array(data['time'])
    state = np.array(data['state'])

    # Plot first pendulum angle
    ax.plot(time, state[:, 2], color=color, linewidth=2, label=label)

ax.axhline(0, color='k', linestyle='--', linewidth=0.5)
ax.set_xlabel('Time (s)', fontsize=14)
ax.set_ylabel('θ₁ (rad)', fontsize=14)
ax.set_title('Controller Comparison: First Pendulum Angle', fontsize=16)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('controller_comparison.png', dpi=300)
plt.show()