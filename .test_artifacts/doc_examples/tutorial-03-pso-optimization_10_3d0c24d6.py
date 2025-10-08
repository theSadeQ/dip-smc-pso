# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 10
# Runnable: False
# Hash: 3d0c24d6

# Check if any particles are improving
pso_log = json.load(open('optimized_gains.json'))
if 'pso_history' in pso_log:
    costs = pso_log['pso_history']['best_costs']
    improvement = (costs[0] - costs[-1]) / costs[0] * 100
    print(f"Total improvement: {improvement:.1f}%")

    if improvement < 5:
        print("WARNING: Minimal improvement. Possible causes:")
        print("1. Bounds too narrow (local minimum)")
        print("2. Cost function not sensitive to gain changes")
        print("3. Default gains already near-optimal")