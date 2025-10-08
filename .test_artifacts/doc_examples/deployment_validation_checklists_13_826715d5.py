# Example from: docs\deployment_validation_checklists.md
# Index: 13
# Runnable: False
# Hash: 826715d5

def validate_system_health():
    """Validate system health after deployment."""
    health_metrics = {
        'cpu_usage': get_cpu_usage(),
        'memory_usage': get_memory_usage(),
        'disk_usage': get_disk_usage(),
        'network_connectivity': test_network_connectivity(),
        'database_health': test_database_health(),
        'application_health': test_application_health()
    }

    # Define acceptable thresholds
    thresholds = {
        'cpu_usage': 80.0,
        'memory_usage': 80.0,
        'disk_usage': 90.0,
        'network_connectivity': True,
        'database_health': True,
        'application_health': True
    }

    # Validate all metrics
    for metric, value in health_metrics.items():
        threshold = thresholds[metric]
        if isinstance(threshold, bool):
            assert value == threshold, f"Health check failed: {metric}"
        else:
            assert value <= threshold, f"Health check failed: {metric} = {value} > {threshold}"

    return health_metrics