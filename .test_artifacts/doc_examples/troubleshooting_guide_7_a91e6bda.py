# Example from: docs\factory\troubleshooting_guide.md
# Index: 7
# Runnable: True
# Hash: a91e6bda

from src.controllers.factory import create_pso_controller_factory, SMCType

def diagnose_pso_factory_error(smc_type):
    print(f"Diagnosing PSO factory for {smc_type}")

    try:
        factory_func = create_pso_controller_factory(smc_type)

        # Check required attributes
        required_attrs = ['n_gains', 'controller_type', 'max_force']
        for attr in required_attrs:
            if hasattr(factory_func, attr):
                value = getattr(factory_func, attr)
                print(f"✓ {attr}: {value}")
            else:
                print(f"✗ Missing attribute: {attr}")

        # Test factory function
        from src.controllers.factory import get_default_gains
        test_gains = get_default_gains(smc_type.value)
        controller = factory_func(test_gains)
        print(f"✓ Factory function test successful")

    except Exception as e:
        print(f"✗ PSO factory creation failed: {e}")

# Example usage
diagnose_pso_factory_error(SMCType.CLASSICAL)