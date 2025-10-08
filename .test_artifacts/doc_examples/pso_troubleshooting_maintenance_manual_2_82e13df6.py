# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 2
# Runnable: True
# Hash: 82e13df6

# Analyze convergence history
import json
import matplotlib.pyplot as plt

with open('optimization_results.json', 'r') as f:
    results = json.load(f)

cost_history = results.get('cost_history', [])
plt.plot(cost_history)
plt.title('PSO Convergence History')
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.show()

# Check final gains against bounds
gains = results['best_gains']
bounds = results.get('bounds', {})
print(f"Final gains: {gains}")
print(f"At lower bound: {[g <= b+0.001 for g, b in zip(gains, bounds.get('lower', []))]}")
print(f"At upper bound: {[g >= b-0.001 for g, b in zip(gains, bounds.get('upper', []))]}")