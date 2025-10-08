# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 17
# Runnable: True
# Hash: fd01ce5d

import matplotlib.pyplot as plt

result = tuner.optimise()

# Plot convergence curve
plt.figure(figsize=(10, 6))
plt.semilogy(result['history']['cost'], linewidth=2)
plt.xlabel('Iteration')
plt.ylabel('Best Cost (log scale)')
plt.title('PSO Convergence History')
plt.grid(True, alpha=0.3)
plt.show()

# Check for premature convergence
if np.std(result['history']['cost'][-20:]) < 1e-6:
    print("Warning: PSO may have converged prematurely")