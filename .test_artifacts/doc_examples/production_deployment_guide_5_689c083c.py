# Example from: docs\factory\production_deployment_guide.md
# Index: 5
# Runnable: True
# Hash: 689c083c

class FactoryPerformanceMonitor:
    """Production performance monitoring for factory system."""

    def __init__(self):
        self.metrics = {
            'controller_creation_time': [],
            'controller_creation_rate': [],
            'error_rate': [],
            'memory_usage': [],
            'thread_contention': [],
            'cache_hit_rate': []
        }

    def collect_metrics(self):
        """Collect current performance metrics."""

        import time
        import psutil
        import os
        from src.controllers.factory import create_controller

        # Controller creation time
        start_time = time.perf_counter()
        try:
            create_controller('classical_smc', gains=[20]*6)
            creation_time = (time.perf_counter() - start_time) * 1000
            self.metrics['controller_creation_time'].append(creation_time)
        except Exception:
            self.metrics['error_rate'].append(1)

        # Memory usage
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        self.metrics['memory_usage'].append(memory_mb)

        # Keep only recent metrics (last 1000 samples)
        for metric_name in self.metrics:
            if len(self.metrics[metric_name]) > 1000:
                self.metrics[metric_name] = self.metrics[metric_name][-1000:]

    def get_metrics_summary(self):
        """Generate metrics summary for monitoring dashboard."""

        import statistics

        summary = {}

        for metric_name, values in self.metrics.items():
            if values:
                summary[metric_name] = {
                    'current': values[-1],
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }

                if len(values) > 1:
                    summary[metric_name]['std'] = statistics.stdev(values)

        return summary

    def check_alert_thresholds(self):
        """Check if any metrics exceed alert thresholds."""

        alerts = []
        thresholds = {
            'controller_creation_time': {'max': 10.0},  # 10ms
            'error_rate': {'max': 0.01},  # 1%
            'memory_usage': {'max': 1000.0},  # 1GB
        }

        summary = self.get_metrics_summary()

        for metric_name, threshold in thresholds.items():
            if metric_name in summary:
                current_value = summary[metric_name]['current']
                max_threshold = threshold.get('max')

                if max_threshold and current_value > max_threshold:
                    alerts.append({
                        'metric': metric_name,
                        'current': current_value,
                        'threshold': max_threshold,
                        'severity': 'critical' if current_value > max_threshold * 2 else 'warning'
                    })

        return alerts

# Setup monitoring
monitor = FactoryPerformanceMonitor()

# Continuous monitoring loop (would run in separate thread)
def monitoring_loop():
    while True:
        monitor.collect_metrics()
        alerts = monitor.check_alert_thresholds()

        if alerts:
            for alert in alerts:
                print(f"ALERT: {alert['metric']} = {alert['current']} > {alert['threshold']}")

        time.sleep(60)  # Collect metrics every minute