# Example from: docs\workflows\complete_integration_guide.md
# Index: 17
# Runnable: True
# Hash: 2a6c175a

# Continuous system health monitoring
from src.monitoring import SystemHealthMonitor

class HealthMonitoringWorkflow:
    """Comprehensive system health monitoring."""

    def __init__(self):
        self.monitor = SystemHealthMonitor(
            check_interval=10.0,  # 10 seconds
            alert_thresholds={
                'cpu_usage': 0.8,
                'memory_usage': 0.9,
                'control_latency': 0.01,
                'error_rate': 0.05
            }
        )

    def start_monitoring(self):
        """Start continuous health monitoring."""

        health_checks = [
            'controller_responsiveness',
            'memory_usage',
            'cpu_utilization',
            'network_connectivity',
            'sensor_data_quality',
            'actuator_functionality',
            'safety_system_status'
        ]

        self.monitor.start_continuous_monitoring(health_checks)

    def generate_health_report(self):
        """Generate comprehensive health report."""

        report = self.monitor.generate_health_report()

        # System status summary
        print(f"🏥 System Health Report")
        print(f"Overall Status: {'✅ HEALTHY' if report.overall_healthy else '❌ ISSUES DETECTED'}")
        print(f"Uptime: {report.uptime}")
        print(f"Last Check: {report.last_check}")

        # Component health
        for component, status in report.component_health.items():
            status_icon = "✅" if status.healthy else "❌"
            print(f"{status_icon} {component}: {status.message}")

        return report