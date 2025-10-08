# Example from: docs\deployment_validation_checklists.md
# Index: 5
# Runnable: False
# Hash: 8636eb7d

def test_configuration_integration():
    """Test configuration system integration."""
    # Test configuration loading
    config = load_config('config.yaml')
    assert validate_configuration_schema(config)

    # Test parameter propagation
    controller = create_controller_from_config(config)
    assert controller.gains == config['controllers']['classical_smc']['gains']

    # Test configuration updates
    updated_config = update_configuration(config, {'optimization': {'max_iterations': 200}})
    assert updated_config['optimization']['max_iterations'] == 200

    return True