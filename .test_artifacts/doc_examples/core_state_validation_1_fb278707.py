# Example from: docs\reference\plant\core_state_validation.md
# Index: 1
# Runnable: True
# Hash: fb278707

def runtime_monitor(x, t):
    if not is_valid(x):
        raise StateValidationError(f"State violation at t={t}")
    if energy_drift(x) > threshold:
        warn(f"Energy drift detected: {energy_drift(x):.2%}")