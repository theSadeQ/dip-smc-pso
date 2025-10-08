# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 9
# Runnable: False
# Hash: 5e442b0e

# example-metadata:
# runnable: false

def test_controller_interface_compliance():
    """Test compliance with BaseController interface."""
    controller = create_test_controller()

    # Test required properties
    assert hasattr(controller, 'gains'), "Must expose gains property"
    assert hasattr(controller, 'n_gains'), "Must declare n_gains for PSO"
    assert controller.n_gains == 6, "Classical SMC requires 6 gains"

    # Test required methods
    assert hasattr(controller, 'compute_control'), "Must implement compute_control"
    assert hasattr(controller, 'reset'), "Must implement reset"
    assert hasattr(controller, 'initialize_state'), "Must implement initialize_state"
    assert hasattr(controller, 'initialize_history'), "Must implement initialize_history"

    # Test gains property returns copy
    gains1 = controller.gains
    gains2 = controller.gains
    assert gains1 == gains2, "Gains should be consistent"

    gains1[0] = 999.0  # Try to mutate
    assert controller.gains[0] != 999.0, "Gains property should return copy"