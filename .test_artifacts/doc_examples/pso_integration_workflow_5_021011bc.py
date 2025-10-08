# Example from: docs\factory\pso_integration_workflow.md
# Index: 5
# Runnable: False
# Hash: 021011bc

# example-metadata:
# runnable: false

class ParallelPSOEvaluator:
    """
    Thread-safe parallel evaluation system for PSO optimization.

    Features:
    - Multi-threaded fitness evaluation
    - Load balancing across CPU cores
    - Memory-efficient swarm processing
    - Progress monitoring and early termination
    """

    def __init__(
        self,
        controller_factory: Callable,
        fitness_function: Callable,
        n_threads: int = 4,
        batch_size: int = 8
    ):
        self.controller_factory = controller_factory
        self.fitness_function = fitness_function
        self.n_threads = n_threads
        self.batch_size = batch_size

        # Thread management
        self.thread_pool = ThreadPoolExecutor(max_workers=n_threads)
        self.evaluation_lock = threading.RLock()

        # Performance monitoring
        self.evaluation_times = []
        self.success_count = 0
        self.failure_count = 0

    def evaluate_swarm_parallel(
        self,
        swarm_positions: np.ndarray,
        timeout_seconds: float = 30.0
    ) -> List[float]:
        """
        Evaluate entire swarm in parallel with timeout protection.

        Args:
            swarm_positions: Array of shape (swarm_size, n_dimensions)
            timeout_seconds: Maximum time for evaluation

        Returns:
            List of fitness values for each particle
        """

        swarm_size = swarm_positions.shape[0]
        fitness_values = [float('inf')] * swarm_size

        # Submit evaluation tasks
        future_to_index = {}

        for i in range(swarm_size):
            future = self.thread_pool.submit(
                self._evaluate_particle_safe,
                swarm_positions[i],
                i
            )
            future_to_index[future] = i

        # Collect results with timeout
        completed_count = 0
        start_time = time.time()

        for future in as_completed(future_to_index, timeout=timeout_seconds):
            try:
                particle_index = future_to_index[future]
                fitness_value = future.result(timeout=1.0)  # Individual timeout
                fitness_values[particle_index] = fitness_value

                with self.evaluation_lock:
                    self.success_count += 1
                    completed_count += 1

            except Exception as e:
                particle_index = future_to_index[future]
                logger.warning(f"Particle {particle_index} evaluation failed: {e}")

                with self.evaluation_lock:
                    self.failure_count += 1

                # Use penalty value for failed evaluations
                fitness_values[particle_index] = 5000.0

            # Check for timeout
            if time.time() - start_time > timeout_seconds:
                logger.warning(f"Swarm evaluation timeout after {timeout_seconds}s")
                break

        # Cancel remaining futures
        for future in future_to_index:
            if not future.done():
                future.cancel()

        return fitness_values

    def _evaluate_particle_safe(self, gains: GainsArray, particle_index: int) -> float:
        """Thread-safe particle evaluation with error handling."""

        start_time = time.time()

        try:
            # Create controller
            controller = self.controller_factory(gains)

            # Evaluate fitness
            fitness_value = self.fitness_function(gains, controller)

            # Record evaluation time
            evaluation_time = time.time() - start_time
            with self.evaluation_lock:
                self.evaluation_times.append(evaluation_time)

            return fitness_value

        except Exception as e:
            logger.warning(f"Particle {particle_index} failed: {e}")
            return 3000.0  # High penalty for failures

    def get_evaluation_statistics(self) -> Dict[str, Any]:
        """Get parallel evaluation performance statistics."""

        with self.evaluation_lock:
            total_evaluations = self.success_count + self.failure_count
            success_rate = self.success_count / max(1, total_evaluations)

            avg_time = np.mean(self.evaluation_times) if self.evaluation_times else 0.0
            max_time = np.max(self.evaluation_times) if self.evaluation_times else 0.0

            return {
                'total_evaluations': total_evaluations,
                'success_count': self.success_count,
                'failure_count': self.failure_count,
                'success_rate': success_rate,
                'avg_evaluation_time': avg_time,
                'max_evaluation_time': max_time,
                'total_evaluation_time': sum(self.evaluation_times),
                'parallel_efficiency': avg_time * self.n_threads / max(max_time, 0.001)
            }

    def cleanup(self):
        """Clean up thread pool resources."""
        self.thread_pool.shutdown(wait=True)