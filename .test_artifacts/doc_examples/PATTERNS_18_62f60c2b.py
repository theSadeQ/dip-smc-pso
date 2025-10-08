# Example from: docs\PATTERNS.md
# Index: 18
# Runnable: False
# Hash: 62f60c2b

# example-metadata:
# runnable: false

# src/simulation/engines/vector_sim.py

def run_batch_simulation(controller, dynamics, initial_conditions_batch, dt=0.001):
    """Vectorized batch simulation - process 1000 simulations simultaneously."""
    n_simulations = initial_conditions_batch.shape[0]
    n_steps = int(T / dt)

    # Allocate batch arrays (vectorized storage)
    states_batch = np.zeros((n_simulations, n_steps, 6))  # 1000 x 10000 x 6
    controls_batch = np.zeros((n_simulations, n_steps))

    states_batch[:, 0, :] = initial_conditions_batch

    for i in range(1, n_steps):
        # Vectorized control computation (1000 controllers at once)
        controls_batch[:, i] = controller.compute_control_batch(states_batch[:, i-1, :])

        # Vectorized dynamics integration (1000 integrations at once)
        states_batch[:, i, :] = dynamics.step_batch(states_batch[:, i-1, :],
                                                     controls_batch[:, i], dt)

    return states_batch, controls_batch