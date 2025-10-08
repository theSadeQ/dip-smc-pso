# Example from: docs\api\factory_system_api_reference.md
# Index: 64
# Runnable: True
# Hash: 04c12208

# test_new_controller.py

from src.controllers.factory import create_controller, get_default_gains
import numpy as np

def test_new_controller_creation():
    """Test new controller can be created."""
    # Test with defaults
    controller = create_controller('new_controller')
    assert controller is not None
    assert controller.gains == [10.0, 8.0, 5.0, 3.0]

    # Test with custom gains
    custom_gains = [15.0, 12.0, 8.0, 5.0]
    controller = create_controller('new_controller', gains=custom_gains)
    assert controller.gains == custom_gains

    # Test compute_control
    state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])
    result = controller.compute_control(state, 0.0, {})
    assert 'u' in result
    assert np.isfinite(result['u'])

if __name__ == '__main__':
    test_new_controller_creation()
    print("✓ New controller tests passed")