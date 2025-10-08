# Example from: docs\architecture\controller_system_architecture.md
# Index: 19
# Runnable: False
# Hash: 06225691

# example-metadata:
# runnable: false

class SystemMonitor:
    """Comprehensive system monitoring and observability."""

    def __init__(self, monitoring_config: Dict[str, Any]):
        self.metrics_collector = MetricsCollector(monitoring_config)
        self.health_checker = HealthChecker(monitoring_config)
        self.alert_manager = AlertManager(monitoring_config)

    def monitor_control_loop(
        self,
        control_cycle_data: ControlCycleData
    ) -> MonitoringReport:
        """Monitor single control loop execution."""

        # Collect performance metrics
        metrics = self.metrics_collector.collect_cycle_metrics(control_cycle_data)

        # Assess system health
        health_status = self.health_checker.assess_health(metrics)

        # Check for alert conditions
        alerts = self.alert_manager.check_alerts(metrics, health_status)

        # Create monitoring report
        report = MonitoringReport(
            timestamp=time.time(),
            metrics=metrics,
            health_status=health_status,
            alerts=alerts,
            cycle_data=control_cycle_data
        )

        return report

class MetricsCollector:
    """Collect and aggregate performance metrics."""

    def collect_cycle_metrics(
        self,
        cycle_data: ControlCycleData
    ) -> PerformanceMetrics:
        """Collect metrics for single control cycle."""

        return PerformanceMetrics(
            # Control Performance
            control_effort=abs(cycle_data.control_action),
            settling_error=self._compute_settling_error(cycle_data.state),
            overshoot=self._compute_overshoot(cycle_data.state_history),

            # Computational Performance
            computation_time=cycle_data.computation_time,
            memory_usage=self._get_memory_usage(),
            cpu_utilization=self._get_cpu_utilization(),

            # System Health
            numerical_stability=self._check_numerical_stability(cycle_data),
            error_rate=self._compute_error_rate(),

            # Controller-Specific Metrics
            controller_health=self._assess_controller_health(cycle_data.controller_output)
        )