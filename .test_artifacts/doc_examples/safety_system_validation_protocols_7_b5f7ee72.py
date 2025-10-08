# Example from: docs\safety_system_validation_protocols.md
# Index: 7
# Runnable: False
# Hash: b5f7ee72

def runtime_safety_check(state, control_signal, parameters):
    """Continuous runtime safety validation."""

    # ASSERTION 1: Control signal within safe bounds
    assert np.all(np.abs(control_signal) <= CONTROL_LIMITS), \
        f"Control signal {control_signal} exceeds limits {CONTROL_LIMITS}"

    # ASSERTION 2: Parameters within validated ranges
    assert validate_parameter_bounds(parameters), \
        f"Parameters {parameters} outside validated ranges"

    # ASSERTION 3: System state within operational envelope
    assert validate_state_bounds(state), \
        f"System state {state} outside operational envelope"

    # ASSERTION 4: Stability maintained
    lyapunov_value = compute_lyapunov_function(state)
    assert lyapunov_value >= 0, \
        f"Lyapunov function negative: {lyapunov_value}"