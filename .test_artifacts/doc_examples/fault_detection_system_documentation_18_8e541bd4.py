# Example from: docs\fault_detection_system_documentation.md
# Index: 18
# Runnable: False
# Hash: 8e541bd4

def test_safety_critical_fault_detection():
    """Verify FDI system meets safety requirements."""

    safety_requirements = {
        "max_detection_delay": 50,      # timesteps
        "max_false_alarm_rate": 0.01,   # 1% during normal operation
        "fault_persistence": True,      # Once faulted, remain faulted
        "graceful_degradation": True    # No crashes on model failures
    }

    # Test large fault detection delay
    large_fault = inject_sensor_bias(magnitude=0.5)
    detection_delay = run_fault_scenario(large_fault)
    assert detection_delay <= safety_requirements["max_detection_delay"]

    # Test false alarm rate
    false_alarm_rate = monte_carlo_false_alarm_test(trials=10000)
    assert false_alarm_rate <= safety_requirements["max_false_alarm_rate"]

    # Test fault persistence
    assert test_fault_persistence() == True

    # Test error handling
    assert test_graceful_degradation() == True