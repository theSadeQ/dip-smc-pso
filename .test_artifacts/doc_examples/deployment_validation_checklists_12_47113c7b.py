# Example from: docs\deployment_validation_checklists.md
# Index: 12
# Runnable: False
# Hash: 47113c7b

def execute_smoke_tests():
    """Execute smoke tests immediately after deployment."""
    smoke_tests = [
        test_system_startup,
        test_basic_controller_operation,
        test_configuration_loading,
        test_monitoring_systems,
        test_api_endpoints,
        test_database_connectivity
    ]

    for test in smoke_tests:
        result = test()
        if not result.success:
            raise DeploymentValidationError(f"Smoke test failed: {test.__name__}")

    return True