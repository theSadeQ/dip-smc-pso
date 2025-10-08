# Example from: docs\technical\configuration_schema_reference.md
# Index: 17
# Runnable: False
# Hash: 48372821

# example-metadata:
# runnable: false

def validate_all_configurations():
    """Test configuration validation for all controller types."""

    try:
        # Test valid configurations
        configs = {
            'classical': ClassicalSMCConfig(
                gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
                max_force=150.0,
                boundary_layer=0.02
            ),
            'sta': SuperTwistingSMCConfig(
                gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43],
                max_force=150.0,
                dt=0.001
            ),
            'adaptive': AdaptiveSMCConfig(
                gains=[12.0, 10.0, 6.0, 5.0, 2.5],
                max_force=150.0,
                dt=0.001
            )
        }

        for name, config in configs.items():
            controller = create_controller(name + '_smc', config=config)
            print(f"✅ {name.capitalize()} SMC configuration valid")

    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")

validate_all_configurations()