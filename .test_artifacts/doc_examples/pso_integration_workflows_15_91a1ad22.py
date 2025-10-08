# Example from: docs\technical\pso_integration_workflows.md
# Index: 15
# Runnable: False
# Hash: 91a1ad22

# example-metadata:
# runnable: false

def analyze_convergence(optimization_result):
    """Analyze PSO convergence characteristics."""

    if not optimization_result['success']:
        print("Optimization failed - no convergence analysis available")
        return

    # Extract convergence data
    performance = optimization_result['performance_analysis']

    print("=== Convergence Analysis ===")
    print(f"Converged: {performance['converged']}")
    print(f"Convergence rate: {performance['convergence_rate']:.2e}")
    print(f"Improvement ratio: {performance['improvement_ratio']:.1%}")
    print(f"Cost reduction: {performance['cost_reduction']:.6f}")
    print(f"Iterations completed: {performance['iterations_completed']}")

    # Convergence quality assessment
    if performance['converged']:
        if performance['convergence_rate'] < 1e-6:
            quality = "Excellent"
        elif performance['convergence_rate'] < 1e-4:
            quality = "Good"
        elif performance['convergence_rate'] < 1e-2:
            quality = "Fair"
        else:
            quality = "Poor"

        print(f"Convergence quality: {quality}")
    else:
        print("Warning: Optimization did not converge")

        # Suggest improvements
        if performance['iterations_completed'] >= 100:
            print("  Suggestion: Increase convergence threshold")
        else:
            print("  Suggestion: Increase max_iterations")

# Example usage
result = pso_factory.optimize_controller()
analyze_convergence(result)