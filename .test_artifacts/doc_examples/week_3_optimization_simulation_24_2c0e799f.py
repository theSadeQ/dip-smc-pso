# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 24
# Runnable: False
# Hash: 2c0e799f

# example-metadata:
# runnable: false

@numba.jit(nopython=True, parallel=True)
def batch_integrate(x0_batch, gains_batch, duration, dt):
    """
    Vectorized simulation for PSO fitness evaluation.

    Args:
        x0_batch: Initial states (B, 6)
        gains_batch: Controller gains (B, N_gains)
        duration: Simulation time
        dt: Timestep

    Returns:
        metrics_batch: Performance metrics (B, N_metrics)
    """
    B = x0_batch.shape[0]
    N = int(duration / dt)
    metrics = np.zeros((B, 3))  # ISE, chattering, effort

    for b in numba.prange(B):  # Parallel loop
        x = x0_batch[b]
        ise = 0.0
        chattering = 0.0
        effort = 0.0

        for i in range(N):
            u = compute_control_vectorized(x, gains_batch[b])
            x_next = rk4_step_vectorized(x, u, dt)

            ise += np.sum(x**2) * dt
            if i > 0:
                chattering += np.abs(u - u_prev)
            effort += u**2 * dt

            x = x_next
            u_prev = u

        metrics[b] = [ise, chattering, effort]

    return metrics