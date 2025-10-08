# Example from: docs\factory_integration_documentation.md
# Index: 38
# Runnable: False
# Hash: d27002fc

# example-metadata:
# runnable: false

# Test controller creation
def test_controller_creation():
    controller = create_controller('classical_smc')
    assert hasattr(controller, 'compute_control')
    assert hasattr(controller, 'gains')

# Test gain validation
def test_gain_validation():
    valid_gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
    controller = create_controller('classical_smc', gains=valid_gains)
    assert controller.gains == valid_gains

# Test error handling
def test_invalid_controller_type():
    with pytest.raises(ValueError, match="Unknown controller type"):
        create_controller('invalid_controller')