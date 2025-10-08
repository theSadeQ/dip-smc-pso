# Example from: docs\factory\pso_factory_api_reference.md
# Index: 16
# Runnable: False
# Hash: ee3d8532

# example-metadata:
# runnable: false

class PSOPerformanceMonitor:
    """
    Real-time performance monitoring for PSO-Factory integration.

    Provides comprehensive monitoring of:
    - PSO convergence metrics
    - Controller creation performance
    - Simulation execution times
    - Memory usage tracking
    - Error rate monitoring
    """

    def __init__(self, monitoring_config: Dict[str, Any]):
        self.config = monitoring_config
        self.metrics = {
            'pso_metrics': {
                'total_evaluations': 0,
                'successful_evaluations': 0,
                'failed_evaluations': 0,
                'average_fitness': 0.0,
                'best_fitness': float('inf'),
                'convergence_rate': 0.0
            },
            'performance_metrics': {
                'controller_creation_time': [],
                'simulation_execution_time': [],
                'fitness_computation_time': [],
                'total_optimization_time': 0.0
            },
            'resource_metrics': {
                'peak_memory_usage': 0.0,
                'average_memory_usage': 0.0,
                'cpu_utilization': [],
                'memory_samples': []
            },
            'error_metrics': {
                'creation_failures': 0,
                'simulation_failures': 0,
                'validation_failures': 0,
                'total_errors': 0
            }
        }

        self.start_time = None
        self.monitoring_active = False

    def start_monitoring(self):
        """Start performance monitoring session."""
        import time
        self.start_time = time.time()
        self.monitoring_active = True
        self._reset_metrics()

    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and return complete performance report."""
        import time
        if self.start_time:
            self.metrics['performance_metrics']['total_optimization_time'] = (
                time.time() - self.start_time
            )
        self.monitoring_active = False
        return self.generate_performance_report()

    def log_controller_creation(self, success: bool, creation_time: float):
        """Log controller creation event."""
        if not self.monitoring_active:
            return

        self.metrics['performance_metrics']['controller_creation_time'].append(creation_time)

        if success:
            self.metrics['pso_metrics']['successful_evaluations'] += 1
        else:
            self.metrics['error_metrics']['creation_failures'] += 1
            self.metrics['pso_metrics']['failed_evaluations'] += 1

    def log_simulation_execution(self, success: bool, execution_time: float):
        """Log simulation execution event."""
        if not self.monitoring_active:
            return

        if success:
            self.metrics['performance_metrics']['simulation_execution_time'].append(execution_time)
        else:
            self.metrics['error_metrics']['simulation_failures'] += 1

    def log_fitness_evaluation(self, fitness_value: float, computation_time: float):
        """Log fitness evaluation result."""
        if not self.monitoring_active:
            return

        self.metrics['performance_metrics']['fitness_computation_time'].append(computation_time)
        self.metrics['pso_metrics']['total_evaluations'] += 1

        # Update best fitness
        if fitness_value < self.metrics['pso_metrics']['best_fitness']:
            self.metrics['pso_metrics']['best_fitness'] = fitness_value

        # Update average fitness (running average)
        total_evals = self.metrics['pso_metrics']['total_evaluations']
        current_avg = self.metrics['pso_metrics']['average_fitness']
        self.metrics['pso_metrics']['average_fitness'] = (
            (current_avg * (total_evals - 1) + fitness_value) / total_evals
        )

    def log_resource_usage(self):
        """Log current resource usage."""
        if not self.monitoring_active:
            return

        try:
            import psutil

            # Memory usage
            memory_info = psutil.virtual_memory()
            current_memory = memory_info.percent
            self.metrics['resource_metrics']['memory_samples'].append(current_memory)

            # Update peak memory
            if current_memory > self.metrics['resource_metrics']['peak_memory_usage']:
                self.metrics['resource_metrics']['peak_memory_usage'] = current_memory

            # CPU utilization
            cpu_percent = psutil.cpu_percent(interval=None)
            self.metrics['resource_metrics']['cpu_utilization'].append(cpu_percent)

        except ImportError:
            pass  # psutil not available

    def check_performance_alerts(self) -> List[str]:
        """Check for performance issues and return alerts."""
        alerts = []

        # Memory usage alerts
        if self.metrics['resource_metrics']['peak_memory_usage'] > 90:
            alerts.append(f"High memory usage: {self.metrics['resource_metrics']['peak_memory_usage']:.1f}%")

        # Error rate alerts
        total_evals = self.metrics['pso_metrics']['total_evaluations']
        if total_evals > 0:
            error_rate = self.metrics['error_metrics']['total_errors'] / total_evals
            if error_rate > 0.1:
                alerts.append(f"High error rate: {error_rate:.1%}")

        # Performance alerts
        creation_times = self.metrics['performance_metrics']['controller_creation_time']
        if creation_times and np.mean(creation_times) > 0.002:  # 2ms threshold
            alerts.append(f"Slow controller creation: {np.mean(creation_times)*1000:.2f}ms average")

        return alerts

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""

        # Calculate derived metrics
        total_evals = self.metrics['pso_metrics']['total_evaluations']
        success_rate = (self.metrics['pso_metrics']['successful_evaluations'] / total_evals * 100
                       if total_evals > 0 else 0)

        creation_times = self.metrics['performance_metrics']['controller_creation_time']
        avg_creation_time = np.mean(creation_times) if creation_times else 0

        simulation_times = self.metrics['performance_metrics']['simulation_execution_time']
        avg_simulation_time = np.mean(simulation_times) if simulation_times else 0

        fitness_times = self.metrics['performance_metrics']['fitness_computation_time']
        avg_fitness_time = np.mean(fitness_times) if fitness_times else 0

        memory_samples = self.metrics['resource_metrics']['memory_samples']
        avg_memory = np.mean(memory_samples) if memory_samples else 0

        cpu_samples = self.metrics['resource_metrics']['cpu_utilization']
        avg_cpu = np.mean(cpu_samples) if cpu_samples else 0

        total_time = self.metrics['performance_metrics']['total_optimization_time']
        evaluations_per_second = total_evals / total_time if total_time > 0 else 0

        # Generate report
        report = {
            'summary': {
                'total_evaluations': total_evals,
                'success_rate': success_rate,
                'best_fitness_achieved': self.metrics['pso_metrics']['best_fitness'],
                'total_optimization_time': total_time,
                'evaluations_per_second': evaluations_per_second
            },
            'performance': {
                'average_controller_creation_time_ms': avg_creation_time * 1000,
                'average_simulation_time_ms': avg_simulation_time * 1000,
                'average_fitness_computation_time_ms': avg_fitness_time * 1000
            },
            'resources': {
                'peak_memory_usage_percent': self.metrics['resource_metrics']['peak_memory_usage'],
                'average_memory_usage_percent': avg_memory,
                'average_cpu_utilization_percent': avg_cpu
            },
            'errors': {
                'controller_creation_failures': self.metrics['error_metrics']['creation_failures'],
                'simulation_failures': self.metrics['error_metrics']['simulation_failures'],
                'validation_failures': self.metrics['error_metrics']['validation_failures'],
                'total_error_count': self.metrics['error_metrics']['total_errors']
            },
            'alerts': self.check_performance_alerts(),
            'raw_metrics': self.metrics
        }

        return report

    def _reset_metrics(self):
        """Reset all metrics for new monitoring session."""
        for category in self.metrics.values():
            if isinstance(category, dict):
                for key, value in category.items():
                    if isinstance(value, list):
                        category[key] = []
                    elif isinstance(value, (int, float)):
                        if 'best_fitness' in key:
                            category[key] = float('inf')
                        else:
                            category[key] = 0

# Context manager for automatic monitoring
@contextmanager
def monitor_pso_performance(config: Dict[str, Any] = None):
    """
    Context manager for automatic PSO performance monitoring.

    Usage:
        with monitor_pso_performance() as monitor:
            # Run PSO optimization
            result = optimize_controller_with_pso(...)

        # Get performance report
        report = monitor.generate_performance_report()
    """
    monitor = PSOPerformanceMonitor(config or {})
    monitor.start_monitoring()

    try:
        yield monitor
    finally:
        monitor.stop_monitoring()