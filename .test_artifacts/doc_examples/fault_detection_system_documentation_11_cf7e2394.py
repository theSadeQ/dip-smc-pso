# Example from: docs\fault_detection_system_documentation.md
# Index: 11
# Runnable: True
# Hash: cf7e2394

if current_state == "OK":
    if residual > hysteresis_upper for persistence_counter steps:
        transition to "FAULT"
elif current_state == "FAULT":
    # Current: persistent (no automatic recovery)
    # Future: if residual < hysteresis_lower: transition to "OK"
    pass