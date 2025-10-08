# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 10
# Runnable: True
# Hash: 4867c0a9

import pickle
import os

def pso_with_checkpointing(checkpoint_interval=10):
    """
    Run PSO with periodic checkpoints.
    """
    checkpoint_file = 'pso_checkpoint.pkl'

    # Load checkpoint if exists
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'rb') as f:
            checkpoint = pickle.load(f)
        print(f"Resuming from iteration {checkpoint['iteration']}")
        start_iter = checkpoint['iteration']
        best_gains = checkpoint['best_gains']
        best_cost = checkpoint['best_cost']
    else:
        start_iter = 0
        best_gains = None
        best_cost = float('inf')

    # Run PSO (pseudo-code, adapt to your PSO implementation)
    for iteration in range(start_iter, 100):
        # PSO update step
        gains, cost = pso_step(iteration)

        if cost < best_cost:
            best_cost = cost
            best_gains = gains

        # Checkpoint every N iterations
        if (iteration + 1) % checkpoint_interval == 0:
            checkpoint = {
                'iteration': iteration + 1,
                'best_gains': best_gains,
                'best_cost': best_cost
            }
            with open(checkpoint_file, 'wb') as f:
                pickle.dump(checkpoint, f)
            print(f"Checkpoint saved at iteration {iteration + 1}")

    # Clean up checkpoint
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

    return best_gains, best_cost