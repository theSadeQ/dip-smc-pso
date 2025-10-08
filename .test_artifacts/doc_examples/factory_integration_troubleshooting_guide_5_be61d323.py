# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 5
# Runnable: True
# Hash: be61d323

def check_controller_dependencies():
    """Check which controllers are available and why others aren't."""

    from src.controllers.factory import CONTROLLER_REGISTRY

    for controller_type, info in CONTROLLER_REGISTRY.items():
        if info['class'] is None:
            print(f"❌ {controller_type}: Class not available")

            if controller_type == 'mpc_controller':
                print("   Reason: Optional MPC dependencies not installed")
                print("   Solution: pip install control-systems-toolkit")
        else:
            print(f"✅ {controller_type}: Available")

check_controller_dependencies()