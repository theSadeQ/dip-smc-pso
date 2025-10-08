# Example from: docs\api\factory_system_api_reference.md
# Index: 69
# Runnable: True
# Hash: 8d7c441d

"""
Example 5: Error Handling and Validation
Demonstrates robust error handling patterns.
"""

from src.controllers.factory import (
    create_controller,
    list_available_controllers,
    get_default_gains,
    FactoryConfigurationError
)
from src.config import load_config
import numpy as np

def safe_controller_creation(controller_type, config=None, gains=None):
    """Create controller with comprehensive error handling."""
    try:
        # Pre-flight checks
        if controller_type not in list_available_controllers():
            print(f"⚠ Warning: {controller_type} not available")
            return None, "Controller type unavailable"

        # Attempt creation
        controller = create_controller(controller_type, config, gains)
        return controller, None

    except ValueError as e:
        return None, f"Validation error: {e}"

    except ImportError as e:
        return None, f"Dependency error: {e}"

    except FactoryConfigurationError as e:
        return None, f"Configuration error: {e}"

    except Exception as e:
        return None, f"Unexpected error: {e}"

def main():
    config = load_config("config.yaml")

    print("Demonstrating error handling patterns\n")
    print("="*80)

    # Test 1: Valid creation
    print("\nTest 1: Valid controller creation")
    controller, error = safe_controller_creation('classical_smc', config)
    if controller:
        print("  ✓ Success: Controller created")
    else:
        print(f"  ✗ Failed: {error}")

    # Test 2: Invalid controller type
    print("\nTest 2: Invalid controller type")
    controller, error = safe_controller_creation('nonexistent_controller', config)
    if controller:
        print("  ✓ Success: Controller created")
    else:
        print(f"  ✗ Expected failure: {error}")

    # Test 3: Invalid gain count
    print("\nTest 3: Invalid gain count")
    invalid_gains = [10.0, 20.0]  # Only 2 gains, need 6
    controller, error = safe_controller_creation('classical_smc', config, invalid_gains)
    if controller:
        print("  ✓ Success: Controller created")
    else:
        print(f"  ✗ Expected failure: {error}")

    # Test 4: Invalid gain values (non-positive)
    print("\nTest 4: Invalid gain values (non-positive)")
    invalid_gains = [10.0, -5.0, 12.0, 8.0, 35.0, 5.0]  # Negative gain
    controller, error = safe_controller_creation('classical_smc', config, invalid_gains)
    if controller:
        print("  ✓ Success: Controller created")
    else:
        print(f"  ✗ Expected failure: {error}")

    # Test 5: Super-twisting constraint violation
    print("\nTest 5: Super-twisting K1 > K2 constraint")
    invalid_sta_gains = [15.0, 20.0, 12.0, 8.0, 6.0, 4.0]  # K1=15 ≤ K2=20
    controller, error = safe_controller_creation('sta_smc', config, invalid_sta_gains)
    if controller:
        print("  ✓ Success: Controller created")
    else:
        print(f"  ✗ Expected failure: {error}")

    # Test 6: Valid super-twisting gains
    print("\nTest 6: Valid super-twisting gains")
    valid_sta_gains = [30.0, 18.0, 22.0, 14.0, 9.0, 7.0]  # K1=30 > K2=18 ✓
    controller, error = safe_controller_creation('sta_smc', config, valid_sta_gains)
    if controller:
        print("  ✓ Success: Controller created with K1 > K2")
    else:
        print(f"  ✗ Failed: {error}")

    # Test 7: Adaptive SMC gain count validation
    print("\nTest 7: Adaptive SMC gain count (must be exactly 5)")
    invalid_adaptive_gains = [10.0, 8.0, 5.0, 4.0, 1.0, 0.5]  # 6 gains, need 5
    controller, error = safe_controller_creation('adaptive_smc', config, invalid_adaptive_gains)
    if controller:
        print("  ✓ Success: Controller created")
    else:
        print(f"  ✗ Expected failure: {error}")

    # Test 8: Recovery with default gains
    print("\nTest 8: Recovery with default gains")
    default_gains = get_default_gains('classical_smc')
    controller, error = safe_controller_creation('classical_smc', config, default_gains)
    if controller:
        print(f"  ✓ Success: Controller created with defaults {default_gains}")
    else:
        print(f"  ✗ Failed: {error}")

    print("\n" + "="*80)
    print("Error handling demonstration complete")

if __name__ == '__main__':
    main()