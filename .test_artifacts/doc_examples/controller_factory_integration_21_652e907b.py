# Example from: docs\technical\controller_factory_integration.md
# Index: 21
# Runnable: True
# Hash: 652e907b

def validate_memory_usage():
    """Validate factory memory usage patterns."""

    import psutil
    import gc

    # Baseline memory
    gc.collect()
    baseline = psutil.Process().memory_info().rss

    # Create multiple controllers
    controllers = []
    for i in range(100):
        controller = create_controller('classical_smc')
        controllers.append(controller)

        if i % 10 == 0:
            current = psutil.Process().memory_info().rss
            memory_per_controller = (current - baseline) / (i + 1)
            assert memory_per_controller < 1_000_000  # < 1MB per controller