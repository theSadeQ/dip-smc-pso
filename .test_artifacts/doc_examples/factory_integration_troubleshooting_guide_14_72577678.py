# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 14
# Runnable: True
# Hash: 72577678

def debug_configuration_priority(controller_type, config=None, gains=None, **kwargs):
    """Debug configuration parameter resolution."""

    print(f"Configuration priority debug for {controller_type}:")
    print(f"Parameters provided:")
    print(f"  gains: {gains}")
    print(f"  config: {config is not None}")
    print(f"  kwargs: {kwargs}")
    print()

    # Priority 1: Explicit gains
    if gains is not None:
        print(f"✅ Priority 1 - Explicit gains: {gains}")
        final_gains = gains
    else:
        # Priority 2: Configuration object
        config_gains = None
        if config is not None:
            try:
                # Try different config structures
                if hasattr(config, 'controllers') and controller_type in config.controllers:
                    controller_config = config.controllers[controller_type]
                    if hasattr(controller_config, 'gains'):
                        config_gains = controller_config.gains
                        print(f"✅ Priority 2 - Config gains: {config_gains}")
            except Exception as e:
                print(f"❌ Config extraction failed: {e}")

        if config_gains is not None:
            final_gains = config_gains
        else:
            # Priority 3: Registry defaults
            from src.controllers.factory import get_default_gains
            default_gains = get_default_gains(controller_type)
            print(f"✅ Priority 3 - Default gains: {default_gains}")
            final_gains = default_gains

    print(f"\nFinal gains: {final_gains}")
    return final_gains

# Test configuration priority
from src.config import load_config
config = load_config("config.yaml")

gains = debug_configuration_priority(
    'classical_smc',
    config=config,
    gains=[25, 20, 15, 10, 40, 6]  # Should override config
)