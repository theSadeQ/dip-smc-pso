# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 14
# Runnable: False
# Hash: ff1cc65f

# example-metadata:
# runnable: false

def optimization_callback(iteration, best_cost, best_position, **kwargs):
    """Real-time optimization monitoring callback."""

    # Log progress
    print(f"Iteration {iteration:3d}: Cost = {best_cost:.6f}")

    # Update visualization
    plt.scatter(iteration, best_cost, c='blue', alpha=0.7)
    plt.xlabel('Iteration')
    plt.ylabel('Best Cost')
    plt.pause(0.01)

    # Save intermediate results
    if iteration % 20 == 0:
        save_checkpoint(iteration, best_position, best_cost)

    # Early stopping condition
    if best_cost < 10.0:  # Target achieved
        return True  # Stop optimization

    return False  # Continue optimization

# Use callback in optimization
results = pso_tuner.optimize(
    bounds=bounds,
    callback=optimization_callback,
    n_particles=50,
    n_iterations=200
)