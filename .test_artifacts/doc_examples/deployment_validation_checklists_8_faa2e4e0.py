# Example from: docs\deployment_validation_checklists.md
# Index: 8
# Runnable: False
# Hash: faa2e4e0

def test_fault_tolerance():
    """Test system fault tolerance."""
    system = ControlSystem()

    # Test controller failure recovery
    system.inject_fault('controller_failure')
    assert system.enter_safe_mode()
    assert system.recover_from_fault('controller_failure')

    # Test sensor failure handling
    system.inject_fault('sensor_failure')
    assert system.switch_to_backup_sensors()

    # Test network interruption handling
    system.inject_fault('network_interruption')
    assert system.maintain_operation_offline()

    return True