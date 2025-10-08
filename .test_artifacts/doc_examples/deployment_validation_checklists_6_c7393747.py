# Example from: docs\deployment_validation_checklists.md
# Index: 6
# Runnable: False
# Hash: c7393747

# example-metadata:
# runnable: false

def test_monitoring_integration():
    """Test monitoring system integration."""
    monitor = SystemMonitor()

    # Test metric collection
    metrics = monitor.collect_metrics()
    required_metrics = ['cpu_usage', 'memory_usage', 'control_frequency', 'stability_margin']
    assert all(metric in metrics for metric in required_metrics)

    # Test alerting system
    monitor.set_threshold('cpu_usage', 80.0)
    monitor.simulate_high_cpu()
    alerts = monitor.get_active_alerts()
    assert any(alert.type == 'cpu_usage' for alert in alerts)

    return True