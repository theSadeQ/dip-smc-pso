# Example from: docs\fault_detection_system_documentation.md
# Index: 4
# Runnable: False
# Hash: 46da0b75

# example-metadata:
# runnable: false

fault_test_matrix = {
    "sensor_bias": {
        "magnitude": np.array([0.1, 0.0, 0.0, 0.0]),
        "expected_detection_time": "<50 timesteps",
        "method": "threshold_based"
    },
    "parameter_drift": {
        "evolution": "linear_drift(rate=0.001)",
        "expected_detection_time": "<100 timesteps",
        "method": "cusum_based"
    },
    "intermittent_fault": {
        "pattern": "periodic_dropout(period=20)",
        "expected_behavior": "no_false_alarms",
        "method": "persistence_filtering"
    }
}