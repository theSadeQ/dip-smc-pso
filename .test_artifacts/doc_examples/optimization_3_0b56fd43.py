# Example from: docs\guides\api\optimization.md
# Index: 3
# Runnable: True
# Hash: 0b56fd43

# Enable convergence tracking
history = tuner.optimize(track_convergence=True)

best_gains = history['best_gains']
best_cost = history['best_cost']
convergence = history['convergence']

# Plot convergence
import matplotlib.pyplot as plt

plt.plot(convergence)
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.title('PSO Convergence')
plt.grid(True)
plt.show()