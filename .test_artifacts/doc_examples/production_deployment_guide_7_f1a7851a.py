# Example from: docs\factory\production_deployment_guide.md
# Index: 7
# Runnable: False
# Hash: f1a7851a

class FactoryAlertManager:
    """Production alerting for factory system."""

    def __init__(self, config):
        self.config = config
        self.alert_history = []
        self.suppression_rules = {}

    def evaluate_alerts(self, metrics, health_status):
        """Evaluate alert conditions."""

        alerts = []

        # Performance alerts
        if 'controller_creation_time' in metrics:
            avg_time = metrics['controller_creation_time']['mean']
            if avg_time > 10:  # 10ms threshold
                alerts.append({
                    'type': 'performance',
                    'severity': 'warning' if avg_time < 20 else 'critical',
                    'message': f'High controller creation time: {avg_time:.2f}ms',
                    'metric': 'controller_creation_time',
                    'value': avg_time,
                    'threshold': 10
                })

        # Memory alerts
        if 'memory_usage' in metrics:
            memory_mb = metrics['memory_usage']['current']
            if memory_mb > 500:  # 500MB threshold
                alerts.append({
                    'type': 'memory',
                    'severity': 'warning' if memory_mb < 1000 else 'critical',
                    'message': f'High memory usage: {memory_mb:.2f}MB',
                    'metric': 'memory_usage',
                    'value': memory_mb,
                    'threshold': 500
                })

        # Health alerts
        if health_status['overall_status'] != 'healthy':
            failed_checks = [name for name, check in health_status['checks'].items()
                           if not check.get('healthy', False)]

            alerts.append({
                'type': 'health',
                'severity': 'critical' if health_status['overall_status'] == 'unhealthy' else 'warning',
                'message': f'Health check failed: {", ".join(failed_checks)}',
                'failed_checks': failed_checks
            })

        # Apply suppression rules
        alerts = self.apply_suppression(alerts)

        # Send notifications
        for alert in alerts:
            self.send_notification(alert)

        return alerts

    def apply_suppression(self, alerts):
        """Apply alert suppression rules."""

        suppressed_alerts = []

        for alert in alerts:
            alert_key = f"{alert['type']}_{alert.get('metric', 'unknown')}"

            # Check if alert is already suppressed
            if alert_key in self.suppression_rules:
                last_sent = self.suppression_rules[alert_key]
                if time.time() - last_sent < 300:  # 5 minute suppression
                    continue

            suppressed_alerts.append(alert)
            self.suppression_rules[alert_key] = time.time()

        return suppressed_alerts

    def send_notification(self, alert):
        """Send alert notification."""

        print(f"🚨 ALERT [{alert['severity'].upper()}]: {alert['message']}")

        # In production, integrate with:
        # - Slack/Teams notifications
        # - PagerDuty
        # - Email alerts
        # - SMS notifications
        # - Monitoring dashboards

        self.alert_history.append({
            'timestamp': time.time(),
            'alert': alert
        })

# Setup alert manager
alert_manager = FactoryAlertManager(production_config)