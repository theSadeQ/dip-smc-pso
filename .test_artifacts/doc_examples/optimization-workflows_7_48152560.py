# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 7
# Runnable: True
# Hash: 48152560

# Check cost volatility
cost_changes = np.diff(best_costs)
volatility = np.std(cost_changes)

if volatility > 0.1 * np.mean(best_costs):
    print("WARNING: High convergence volatility")
    print(f"  Volatility: {volatility:.4f}")