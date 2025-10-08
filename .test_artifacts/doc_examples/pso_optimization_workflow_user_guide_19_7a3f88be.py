# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 19
# Runnable: True
# Hash: 7a3f88be

# Save intermediate results every 20 iterations
def checkpoint_callback(iteration, best_position, best_cost, **kwargs):
    if iteration % 20 == 0:
        np.save(f'checkpoint_{iteration}.npy', {
            'iteration': iteration,
            'best_position': best_position,
            'best_cost': best_cost
        })