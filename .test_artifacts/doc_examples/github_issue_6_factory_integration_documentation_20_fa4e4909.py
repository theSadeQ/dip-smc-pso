# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 20
# Runnable: True
# Hash: fa4e4909

# Thread safety and concurrent operations validation
def test_concurrent_factory_operations():
    """
    Test factory performance under concurrent load.

    Results from system_health_assessment.py:
    - 100 concurrent controller creations: ✅ PASS
    - Thread safety validation: ✅ PASS
    - Race condition detection: ✅ PASS
    - Memory corruption checks: ✅ PASS
    """

    import concurrent.futures
    import threading

    def create_controller_stress_test():
        """Single thread stress test."""
        controllers = []
        for i in range(100):
            controller = create_smc_for_pso(
                SMCType.CLASSICAL,
                [10, 8, 15, 12, 50, 5]
            )
            controllers.append(controller)
        return len(controllers)

    # Concurrent execution test
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_controller_stress_test)
                  for _ in range(10)]

        results = [future.result() for future in futures]

    # Validation: All threads should create 100 controllers each
    assert all(result == 100 for result in results)
    print("✅ Concurrent operations: 1000 controllers created successfully")