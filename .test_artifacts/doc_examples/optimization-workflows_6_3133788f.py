# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 6
# Runnable: False
# Hash: 3133788f

# example-metadata:
# runnable: false

# Check if swarm collapsed
if 'pso_history' in data:
    final_best = best_costs[-1]
    final_mean = mean_costs[-1]

    diversity_ratio = final_mean / final_best

    if diversity_ratio < 1.05:  # Within 5%
        print("WARNING: Swarm collapsed (premature convergence)")
        print(f"  Best:  {final_best:.4f}")
        print(f"  Mean:  {final_mean:.4f}")
        print(f"  Ratio: {diversity_ratio:.3f}")
    else:
        print("OK: Swarm maintains diversity")