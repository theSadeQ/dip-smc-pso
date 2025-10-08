# Example from: docs\fault_detection_system_documentation.md
# Index: 5
# Runnable: False
# Hash: b7a64c2c

# example-metadata:
# runnable: false

def validate_false_alarm_rate(n_trials=10000):
    """Validate false alarm rate under normal conditions."""
    false_alarms = 0
    for trial in range(n_trials):
        fdi = FDIsystem(residual_threshold=0.1)
        # Generate normal operation data with known statistics
        for measurement in generate_normal_data():
            status, _ = fdi.check(...)
            if status == "FAULT":
                false_alarms += 1
                break

    actual_far = false_alarms / n_trials
    theoretical_far = compute_theoretical_far()

    assert abs(actual_far - theoretical_far) < 0.01  # 1% tolerance