# Example from: docs\deployment_validation_checklists.md
# Index: 11
# Runnable: False
# Hash: 6ef2c0e0

def test_hardware_safety_integration():
    """Test hardware safety system integration."""
    safety_system = HardwareSafetySystem()

    # Test emergency stop hardware
    assert safety_system.test_emergency_stop_button()
    assert safety_system.emergency_stop_response_time < 0.050  # 50ms

    # Test hardware limits
    assert safety_system.test_position_limits()
    assert safety_system.test_velocity_limits()
    assert safety_system.test_acceleration_limits()

    # Test safety interlocks
    assert safety_system.test_safety_interlocks()

    return True