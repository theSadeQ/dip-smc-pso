# Example from: docs\PATTERNS.md
# Index: 7
# Runnable: True
# Hash: a5a196e6

# Register observers
health_monitor.register_observer(logger_observer)
health_monitor.register_observer(alert_system_observer)
health_monitor.register_observer(dashboard_observer)

# Status change automatically notifies all observers
component.update_status(HealthStatus.CRITICAL)  # All observers notified