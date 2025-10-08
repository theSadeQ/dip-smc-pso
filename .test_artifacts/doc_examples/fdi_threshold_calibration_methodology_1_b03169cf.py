# Example from: docs\fdi_threshold_calibration_methodology.md
# Index: 1
# Runnable: True
# Hash: b03169cf

if current_state == "OK":
    if residual > hysteresis_upper for persistence_counter consecutive steps:
        transition to "FAULT"
elif current_state == "FAULT":
    # Current: persistent fault (no recovery)
    # Future: if residual < hysteresis_lower: transition to "OK"
    pass