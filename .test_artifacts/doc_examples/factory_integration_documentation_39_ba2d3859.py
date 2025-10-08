# Example from: docs\factory_integration_documentation.md
# Index: 39
# Runnable: False
# Hash: ba2d3859

# Test PSO integration
def test_pso_integration():
    factory = create_pso_controller_factory(SMCType.CLASSICAL)
    assert hasattr(factory, 'n_gains')
    assert hasattr(factory, 'controller_type')

    controller = factory([10, 8, 15, 12, 50, 5])
    assert hasattr(controller, 'validate_gains')
    assert hasattr(controller, 'compute_control')

# Test configuration integration
def test_config_integration():
    config = load_config("config.yaml")
    controller = create_controller('classical_smc', config=config)
    # Verify configuration applied correctly