# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 24
# Runnable: True
# Hash: 7e5e91e3

import pytest

def test_controller_parameter_validation():
    """Test that controller rejects invalid parameters."""

    # Valid parameters should work
    controller = PIDController(kp=10.0, ki=2.0, kd=5.0, u_max=50.0)
    assert controller.kp == 10.0

    # Negative gain should fail
    with pytest.raises(ValueError, match="proportional_gain must be > 0"):
        PIDController(kp=-1.0, ki=2.0, kd=5.0, u_max=50.0)

    # Excessive saturation should fail
    with pytest.raises(ValueError, match="control_saturation must be in the interval"):
        PIDController(kp=10.0, ki=2.0, kd=5.0, u_max=1000.0)