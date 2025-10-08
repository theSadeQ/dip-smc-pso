# Example from: docs\deployment_validation_checklists.md
# Index: 15
# Runnable: False
# Hash: bd3e7be4

# example-metadata:
# runnable: false

def validate_rollback_success():
    """Validate successful rollback to previous version."""
    # Check system is running
    assert check_system_status() == 'running'

    # Verify version rollback
    current_version = get_current_version()
    expected_version = get_previous_version()
    assert current_version == expected_version

    # Run basic functionality tests
    assert test_basic_functionality()

    # Check performance metrics
    metrics = collect_performance_metrics()
    assert metrics['response_time'] < 50  # ms
    assert metrics['error_rate'] < 0.01   # 1%

    return True