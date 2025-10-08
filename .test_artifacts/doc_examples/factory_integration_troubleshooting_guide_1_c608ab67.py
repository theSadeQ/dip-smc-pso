# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 1
# Runnable: False
# Hash: c608ab67

#!/usr/bin/env python3
"""Factory integration quick diagnostic tool."""

import logging
import traceback
from src.controllers.factory import (
    list_available_controllers,
    list_all_controllers,
    create_controller,
    get_default_gains
)

def quick_diagnosis():
    """Run quick diagnostic checks for factory integration."""

    print("=== Factory Integration Diagnostic ===\n")

    # 1. Check available controllers
    print("1. Checking available controllers...")
    try:
        available = list_available_controllers()
        all_controllers = list_all_controllers()
        unavailable = set(all_controllers) - set(available)

        print(f"   ✅ Available: {available}")
        if unavailable:
            print(f"   ⚠️  Unavailable: {unavailable}")
        print()
    except Exception as e:
        print(f"   ❌ Controller listing failed: {e}")
        return False

    # 2. Test basic controller creation
    print("2. Testing basic controller creation...")
    for controller_type in available:
        try:
            controller = create_controller(controller_type)
            print(f"   ✅ {controller_type}: Created successfully")
        except Exception as e:
            print(f"   ❌ {controller_type}: {e}")
    print()

    # 3. Test gain access
    print("3. Testing default gains access...")
    for controller_type in available:
        try:
            gains = get_default_gains(controller_type)
            print(f"   ✅ {controller_type}: {len(gains)} gains")
        except Exception as e:
            print(f"   ❌ {controller_type}: {e}")
    print()

    # 4. Test PSO integration
    print("4. Testing PSO integration...")
    try:
        from src.controllers.factory import create_pso_controller_factory, SMCType
        factory = create_pso_controller_factory(SMCType.CLASSICAL)
        test_gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        controller = factory(test_gains)
        print(f"   ✅ PSO factory: Working")
    except Exception as e:
        print(f"   ❌ PSO factory: {e}")
    print()

    # 5. Test configuration integration
    print("5. Testing configuration integration...")
    try:
        from src.config import load_config
        config = load_config("config.yaml")
        controller = create_controller('classical_smc', config=config)
        print(f"   ✅ Configuration: Working")
    except Exception as e:
        print(f"   ❌ Configuration: {e}")
    print()

    print("=== Diagnostic Complete ===")
    return True

if __name__ == "__main__":
    quick_diagnosis()