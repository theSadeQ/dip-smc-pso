# Example from: docs\factory\troubleshooting_guide.md
# Index: 1
# Runnable: True
# Hash: 78735aeb

from src.controllers.factory import (
    list_available_controllers,
    get_default_gains,
    create_controller
)
import numpy as np

def factory_health_check():
    """Comprehensive factory system health check."""

    print("=== Factory System Health Check ===\n")

    # 1. Check available controllers
    try:
        controllers = list_available_controllers()
        print(f"✓ Available controllers: {controllers}")
    except Exception as e:
        print(f"✗ Controller registry error: {e}")
        return False

    # 2. Test default gains retrieval
    for controller_type in controllers:
        try:
            gains = get_default_gains(controller_type)
            print(f"✓ {controller_type} default gains: {gains}")
        except Exception as e:
            print(f"✗ {controller_type} gains error: {e}")

    # 3. Test controller creation
    test_passed = 0
    total_tests = len(controllers)

    for controller_type in controllers:
        try:
            gains = get_default_gains(controller_type)
            controller = create_controller(controller_type, gains=gains)

            # Test basic functionality
            test_state = np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0])
            result = controller.compute_control(test_state, (), {})

            if hasattr(result, 'u'):
                control_value = result.u
            else:
                control_value = result

            if np.isfinite(control_value):
                print(f"✓ {controller_type} creation and test successful")
                test_passed += 1
            else:
                print(f"✗ {controller_type} produced invalid control: {control_value}")

        except Exception as e:
            print(f"✗ {controller_type} creation failed: {e}")

    # 4. Summary
    success_rate = (test_passed / total_tests) * 100
    print(f"\n=== Summary ===")
    print(f"Controllers tested: {total_tests}")
    print(f"Successful: {test_passed}")
    print(f"Success rate: {success_rate:.1f}%")

    if success_rate >= 95:
        print("✓ Factory system is healthy")
        return True
    elif success_rate >= 75:
        print("⚠ Factory system has minor issues")
        return False
    else:
        print("✗ Factory system has major issues")
        return False

# Run the health check
factory_health_check()