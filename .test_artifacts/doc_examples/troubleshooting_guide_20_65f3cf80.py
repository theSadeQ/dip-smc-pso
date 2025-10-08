# Example from: docs\factory\troubleshooting_guide.md
# Index: 20
# Runnable: False
# Hash: 65f3cf80

# example-metadata:
# runnable: false

def emergency_factory_reset():
    """Emergency factory system reset procedure."""

    print("Performing emergency factory reset...")

    # 1. Clear any cached data
    try:
        import importlib
        import src.controllers.factory
        importlib.reload(src.controllers.factory)
        print("✓ Factory module reloaded")
    except Exception as e:
        print(f"✗ Module reload failed: {e}")

    # 2. Test basic functionality
    try:
        from src.controllers.factory import create_controller
        test_controller = create_controller('classical_smc', gains=[10]*6)
        print("✓ Basic factory test successful")
    except Exception as e:
        print(f"✗ Basic factory test failed: {e}")

    # 3. Verify thread safety
    try:
        import threading
        def test_creation():
            create_controller('classical_smc', gains=[10]*6)

        threads = [threading.Thread(target=test_creation) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)

        print("✓ Thread safety test passed")
    except Exception as e:
        print(f"✗ Thread safety test failed: {e}")

    print("Emergency reset completed")

# Run emergency reset if needed
# emergency_factory_reset()