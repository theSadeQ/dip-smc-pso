# Example from: docs\fault_detection_system_documentation.md
# Index: 20
# Runnable: True
# Hash: 19558d18

OPERATIONAL_LIMITS = {
    "residual_threshold": (1e-6, 1e3),    # Avoid numerical issues
    "persistence_counter": (1, 1000),     # Practical response time limits
    "window_size": (5, 10000),            # Statistical validity vs. memory
    "threshold_factor": (0.1, 10.0),      # Reasonable sensitivity range
    "cusum_threshold": (0.1, 100.0),      # Detection sensitivity bounds
    "max_state_dimension": 50,             # Memory and computation limits
    "max_simulation_time": 1e6             # History storage limits
}