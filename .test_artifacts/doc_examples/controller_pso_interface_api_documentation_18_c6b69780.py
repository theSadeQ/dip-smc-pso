# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 18
# Runnable: False
# Hash: c6b69780

class ControllerBenchmark:
    """Standardized controller benchmarking."""

    @staticmethod
    def benchmark_creation(controller_factory: Callable,
                         gain_samples: List[np.ndarray],
                         n_runs: int = 100) -> Dict[str, float]:
        """Benchmark controller creation time.

        Parameters
        ----------
        controller_factory : Callable
            Factory function to benchmark
        gain_samples : List[np.ndarray]
            Sample gain vectors for testing
        n_runs : int
            Number of benchmark runs

        Returns
        -------
        Dict[str, float]
            Timing statistics
        """
        creation_times = []

        for _ in range(n_runs):
            gains = gain_samples[np.random.randint(len(gain_samples))]

            start_time = perf_counter()
            controller = controller_factory(gains)
            end_time = perf_counter()

            creation_times.append(end_time - start_time)

        return {
            'mean_time': np.mean(creation_times),
            'std_time': np.std(creation_times),
            'min_time': np.min(creation_times),
            'max_time': np.max(creation_times),
            'p95_time': np.percentile(creation_times, 95)
        }

    @staticmethod
    def benchmark_control_computation(controller: PSO_ControllerInterface,
                                    state_samples: List[np.ndarray],
                                    n_runs: int = 1000) -> Dict[str, float]:
        """Benchmark control computation performance."""
        computation_times = []

        for _ in range(n_runs):
            state = state_samples[np.random.randint(len(state_samples))]

            start_time = perf_counter()
            control = controller.compute_control(state)
            end_time = perf_counter()

            computation_times.append(end_time - start_time)

        return {
            'mean_time': np.mean(computation_times),
            'std_time': np.std(computation_times),
            'min_time': np.min(computation_times),
            'max_time': np.max(computation_times),
            'p95_time': np.percentile(computation_times, 95),
            'p99_time': np.percentile(computation_times, 99)
        }