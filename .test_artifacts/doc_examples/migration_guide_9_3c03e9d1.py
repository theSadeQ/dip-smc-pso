# Example from: docs\factory\migration_guide.md
# Index: 9
# Runnable: True
# Hash: 3c03e9d1

def validate_migrated_configuration(config_file_path: str) -> bool:
    """
    Validate that migrated configuration works correctly.

    Returns:
        True if validation passes, False otherwise
    """

    try:
        # Load migrated configuration
        with open(config_file_path, 'r') as f:
            if config_file_path.endswith(('.yml', '.yaml')):
                import yaml
                config_data = yaml.safe_load(f)
            else:
                import json
                config_data = json.load(f)

        # Test controller creation
        from src.controllers.factory import create_controller
        from src.plant.configurations import ConfigurationFactory

        plant_config = ConfigurationFactory.create_default_config("simplified")
        validation_results = {}

        if 'controllers' in config_data:
            for controller_type, controller_config in config_data['controllers'].items():
                try:
                    # Create controller with migrated configuration
                    controller = create_controller(
                        controller_type=controller_type,
                        config=plant_config,
                        gains=controller_config.get('gains')
                    )

                    # Test basic functionality
                    test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])
                    control_output = controller.compute_control(test_state, (), {})

                    validation_results[controller_type] = {
                        'creation_success': True,
                        'control_computation_success': True,
                        'control_value': control_output.u if hasattr(control_output, 'u') else control_output
                    }

                    print(f"✓ {controller_type} validation passed")

                except Exception as e:
                    validation_results[controller_type] = {
                        'creation_success': False,
                        'error': str(e)
                    }
                    print(f"✗ {controller_type} validation failed: {e}")

        # Overall validation result
        all_passed = all(
            result.get('creation_success', False)
            for result in validation_results.values()
        )

        print(f"\nValidation Summary:")
        print(f"Controllers tested: {len(validation_results)}")
        print(f"Successful: {sum(1 for r in validation_results.values() if r.get('creation_success', False))}")
        print(f"Overall result: {'PASS' if all_passed else 'FAIL'}")

        return all_passed

    except Exception as e:
        print(f"Validation error: {e}")
        return False

# Example usage
validation_passed = validate_migrated_configuration("config_migrated.yaml")