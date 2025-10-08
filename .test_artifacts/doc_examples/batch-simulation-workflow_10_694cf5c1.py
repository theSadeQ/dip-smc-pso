# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 10
# Runnable: False
# Hash: 694cf5c1

# example-metadata:
# runnable: false

# Check convergence of mean estimate
def check_convergence(samples, window=100):
    """Check if mean estimate has converged."""
    means = [samples[:i].mean() for i in range(window, len(samples), window)]
    relative_change = np.abs(np.diff(means) / means[:-1])
    return relative_change.max() < 0.01  # 1% threshold

# Example
theta1_samples = results[:, -1, 1]
converged = check_convergence(theta1_samples)
print(f"Convergence: {'✓' if converged else '✗'}")