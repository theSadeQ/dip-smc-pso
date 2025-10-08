# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 10
# Runnable: False
# Hash: 2e0bcbc1

def debug_pso_factory_creation(smc_type):
    """Debug PSO factory creation step by step."""

    print(f"Creating PSO factory for {smc_type.value}...")

    try:
        # Step 1: Check controller availability
        from src.controllers.factory import list_available_controllers
        available = list_available_controllers()
        if smc_type.value not in available:
            print(f"❌ Controller {smc_type.value} not available")
            return None

        # Step 2: Create factory
        factory = create_pso_controller_factory(smc_type)
        print(f"✅ Factory created successfully")

        # Step 3: Test factory attributes
        print(f"   n_gains: {factory.n_gains}")
        print(f"   controller_type: {factory.controller_type}")
        print(f"   max_force: {factory.max_force}")

        # Step 4: Test factory function
        from src.controllers.factory import get_default_gains
        test_gains = get_default_gains(smc_type.value)
        controller = factory(test_gains)
        print(f"✅ Factory function works")

        return factory

    except Exception as e:
        print(f"❌ Factory creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# Debug factory creation
factory = debug_pso_factory_creation(SMCType.CLASSICAL)