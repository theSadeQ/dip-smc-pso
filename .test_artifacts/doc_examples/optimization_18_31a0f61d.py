# Example from: docs\guides\api\optimization.md
# Index: 18
# Runnable: False
# Hash: 31a0f61d

# example-metadata:
# runnable: false

def diagnose_convergence(history):
    """Analyze PSO convergence quality."""
    convergence = history['convergence']

    # Check if converged
    final_cost = convergence[-1]
    improvement = convergence[0] - convergence[-1]
    improvement_percent = (improvement / convergence[0]) * 100

    # Detect premature convergence (plateau early)
    plateau_start = None
    for i in range(len(convergence) - 10):
        if np.std(convergence[i:i+10]) < 0.01 * final_cost:
            plateau_start = i
            break

    diagnostics = {
        'converged': improvement_percent > 20,
        'improvement_percent': improvement_percent,
        'final_cost': final_cost,
        'plateau_start': plateau_start,
        'early_plateau': plateau_start is not None and plateau_start < len(convergence) * 0.3
    }

    return diagnostics

# Use diagnostics
history = tuner.optimize(track_convergence=True)
diag = diagnose_convergence(history)

if diag['early_plateau']:
    print("Warning: PSO converged prematurely. Try:")
    print("  - Increase swarm diversity (larger w)")
    print("  - Increase swarm size (more particles)")
    print("  - Widen search bounds")