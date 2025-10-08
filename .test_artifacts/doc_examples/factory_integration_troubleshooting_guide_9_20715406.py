# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 9
# Runnable: True
# Hash: 20715406

from src.controllers.factory import create_pso_controller_factory, SMCType

def verify_pso_factory(smc_type):
    """Verify PSO factory has required attributes."""

    factory = create_pso_controller_factory(smc_type)

    required_attributes = ['n_gains', 'controller_type', 'max_force']
    for attr in required_attributes:
        if not hasattr(factory, attr):
            print(f"❌ Missing attribute: {attr}")
            return False
        else:
            value = getattr(factory, attr)
            print(f"✅ {attr}: {value}")

    return True

# Test factory
if verify_pso_factory(SMCType.CLASSICAL):
    print("PSO factory is properly configured")