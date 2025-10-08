# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 12
# Runnable: True
# Hash: a2f3fc35

class PSO_ProductionMonitor:
    """
    Production monitoring system for PSO optimization workflows.

    Features:
    - Real-time performance metrics
    - Resource utilization tracking
    - Optimization progress visualization
    - Alert system for anomalies
    """

    def __init__(self, monitoring_config: Dict[str, Any]):
        self.config = monitoring_config
        self.metrics = {
            'optimization_start_time': None,
            'total_evaluations': 0,
            'successful_evaluations': 0,
            'failed_evaluations': 0,
            'average_evaluation_time': 0.0,
            'peak_memory_usage': 0.0,
            'cpu_utilization': [],
            'convergence_rate': 0.0
        }

    def start_optimization(self):
        """Initialize monitoring for new optimization run."""
        self.metrics['optimization_start_time'] = time.time()

    def log_evaluation(self, success: bool, evaluation_time: float):
        """Log individual fitness evaluation."""
        self.metrics['total_evaluations'] += 1

        if success:
            self.metrics['successful_evaluations'] += 1
        else:
            self.metrics['failed_evaluations'] += 1

        # Update average evaluation time
        total_time = (self.metrics['average_evaluation_time'] *
                     (self.metrics['total_evaluations'] - 1) + evaluation_time)
        self.metrics['average_evaluation_time'] = total_time / self.metrics['total_evaluations']

    def check_resource_usage(self):
        """Monitor system resource usage."""
        import psutil

        # Memory usage
        memory_info = psutil.virtual_memory()
        self.metrics['peak_memory_usage'] = max(
            self.metrics['peak_memory_usage'],
            memory_info.percent
        )

        # CPU utilization
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metrics['cpu_utilization'].append(cpu_percent)

        # Check for resource alerts
        if memory_info.percent > 90:
            logger.warning(f"High memory usage: {memory_info.percent}%")

        if cpu_percent > 95:
            logger.warning(f"High CPU usage: {cpu_percent}%")

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive monitoring report."""

        if self.metrics['optimization_start_time'] is None:
            return {'status': 'not_started'}

        elapsed_time = time.time() - self.metrics['optimization_start_time']
        success_rate = (self.metrics['successful_evaluations'] /
                       self.metrics['total_evaluations'] * 100
                       if self.metrics['total_evaluations'] > 0 else 0)

        return {
            'elapsed_time': elapsed_time,
            'total_evaluations': self.metrics['total_evaluations'],
            'success_rate': success_rate,
            'average_evaluation_time': self.metrics['average_evaluation_time'],
            'evaluations_per_second': self.metrics['total_evaluations'] / elapsed_time,
            'peak_memory_usage': self.metrics['peak_memory_usage'],
            'average_cpu_usage': np.mean(self.metrics['cpu_utilization']),
            'status': 'running' if elapsed_time > 0 else 'completed'
        }