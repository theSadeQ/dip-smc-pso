# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 19
# Runnable: True
# Hash: 4ebe7e80

import pytest
from typing import Type

def test_pso_controller_interface_compliance(controller_class: Type[PSO_ControllerInterface],
                                           sample_gains: np.ndarray):
    """Test PSO controller interface compliance.

    Parameters
    ----------
    controller_class : Type[PSO_ControllerInterface]
        Controller class to test
    sample_gains : np.ndarray
        Valid gain vector for testing
    """
    # Test instantiation
    controller = controller_class(sample_gains)

    # Test required properties
    assert hasattr(controller, 'max_force'), "Controller missing max_force property"
    assert isinstance(controller.max_force, (int, float)), "max_force must be numeric"
    assert controller.max_force > 0, "max_force must be positive"

    # Test required methods
    assert hasattr(controller, 'compute_control'), "Controller missing compute_control method"
    assert callable(controller.compute_control), "compute_control must be callable"

    # Test control computation
    test_state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
    control = controller.compute_control(test_state)

    assert isinstance(control, (int, float)), "Control output must be numeric"
    assert abs(control) <= controller.max_force, "Control must respect actuator limits"

    # Test optional validate_gains method
    if hasattr(controller, 'validate_gains'):
        test_particles = np.array([sample_gains, sample_gains])
        mask = controller.validate_gains(test_particles)
        assert mask.shape == (2,), "validate_gains must return boolean mask"
        assert mask.dtype == bool, "validate_gains must return boolean array"

def test_controller_factory_integration(controller_type: str, sample_gains: np.ndarray):
    """Test controller factory integration."""
    from src.controllers.factory import ControllerFactory

    # Test factory creation
    controller = ControllerFactory.create_controller(controller_type, sample_gains)

    # Verify interface compliance
    test_pso_controller_interface_compliance(type(controller), sample_gains)

    # Test multiple creations with same gains
    controller2 = ControllerFactory.create_controller(controller_type, sample_gains)
    assert type(controller) == type(controller2), "Factory must return consistent types"