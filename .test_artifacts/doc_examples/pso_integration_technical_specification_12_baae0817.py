# Example from: docs\pso_integration_technical_specification.md
# Index: 12
# Runnable: False
# Hash: baae0817

# example-metadata:
# runnable: false

class PSO_PerformanceMonitor:
    """
    Real-time performance monitoring for PSO optimization process.
    """

    def __init__(self):
        self.metrics = {
            'iteration_times': [],
            'memory_usage': [],
            'convergence_rate': [],
            'particle_diversity': [],
            'cost_improvement': []
        }

    def monitor_iteration(self, iteration: int, swarm_state: SwarmState) -> None:
        """
        Collect performance metrics for each PSO iteration.
        """
        # Timing metrics
        iteration_time = time.time() - swarm_state.iteration_start_time
        self.metrics['iteration_times'].append(iteration_time)

        # Memory monitoring
        memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
        self.metrics['memory_usage'].append(memory_mb)

        # Convergence rate
        if len(swarm_state.cost_history) >= 2:
            improvement_rate = (swarm_state.cost_history[-2] - swarm_state.cost_history[-1])
            self.metrics['cost_improvement'].append(improvement_rate)

        # Alert on performance degradation
        if iteration_time > 5.0:  # 5-second threshold
            logging.warning(f"Slow iteration {iteration}: {iteration_time:.2f}s")

        if memory_mb > 2048:  # 2GB threshold
            logging.warning(f"High memory usage: {memory_mb:.1f}MB")

    def generate_performance_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive performance analysis report.
        """
        return {
            'average_iteration_time': np.mean(self.metrics['iteration_times']),
            'peak_memory_usage': np.max(self.metrics['memory_usage']),
            'total_optimization_time': np.sum(self.metrics['iteration_times']),
            'convergence_efficiency': self._compute_convergence_efficiency(),
            'performance_bottlenecks': self._identify_bottlenecks(),
            'recommendations': self._generate_optimization_recommendations()
        }