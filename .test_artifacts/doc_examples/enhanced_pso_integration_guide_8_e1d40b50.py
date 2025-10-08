# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 8
# Runnable: True
# Hash: e1d40b50

def gpu_accelerated_pso_evaluation(
    particles: np.ndarray,
    controller_factory: Callable,
    simulation_config: Any
) -> np.ndarray:
    """
    GPU-accelerated fitness evaluation using CuPy/Numba.

    For very large swarm sizes (>100 particles), GPU acceleration
    can provide significant speedup.
    """

    try:
        import cupy as cp
        import numba.cuda as cuda

        # Transfer data to GPU
        gpu_particles = cp.asarray(particles)

        # GPU kernel for parallel simulation
        @cuda.jit
        def evaluate_particles_kernel(particles, fitness_scores):
            idx = cuda.grid(1)
            if idx < particles.shape[0]:
                # GPU-accelerated simulation logic
                fitness_scores[idx] = gpu_simulate_controller(particles[idx])

        # Allocate GPU memory
        gpu_fitness = cp.zeros(len(particles))

        # Launch GPU kernel
        threads_per_block = 256
        blocks_per_grid = (len(particles) + threads_per_block - 1) // threads_per_block

        evaluate_particles_kernel[blocks_per_grid, threads_per_block](
            gpu_particles, gpu_fitness
        )

        # Transfer results back to CPU
        return cp.asnumpy(gpu_fitness)

    except ImportError:
        # Fallback to CPU evaluation
        return parallel_fitness_evaluation(particles, controller_factory, simulation_config)