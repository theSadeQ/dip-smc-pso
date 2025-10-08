# Example from: docs\fault_detection_system_documentation.md
# Index: 3
# Runnable: False
# Hash: 05642144

# Threshold parameters
assert residual_threshold > 0, "Threshold must be positive"
assert persistence_counter >= 1, "Persistence counter must be ≥ 1"

# Adaptive parameters
assert window_size >= 5, "Window size too small for robust statistics"
assert threshold_factor > 0, "Threshold factor must be positive"

# State selection validation
assert all(i >= 0 for i in residual_states), "Invalid state indices"
if residual_weights is not None:
    assert len(residual_weights) == len(residual_states), "Weight/state mismatch"
    assert all(w > 0 for w in residual_weights), "Weights must be positive"