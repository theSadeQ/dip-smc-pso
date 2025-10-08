# Example from: docs\configuration_schema_validation.md
# Index: 10
# Runnable: False
# Hash: 4ea48552

# example-metadata:
# runnable: false

def validate_numerical_stability(simulation_config: dict, controller_config: dict) -> bool:
    """Validate numerical stability constraints."""

    dt = simulation_config['dt']

    # Discrete-time stability for SMC
    if controller_config['type'] == 'classical_smc':
        K = max(controller_config['gains'])  # Maximum switching gain

        # CFL-like condition for SMC
        max_dt = 0.1 / K  # Heuristic bound
        if dt > max_dt:
            raise ValueError(f"Time step {dt} too large for switching gain {K}")

    # Nyquist criterion
    control_bandwidth = 100  # Hz, typical for this system
    nyquist_dt = 1 / (2 * control_bandwidth)
    if dt > nyquist_dt:
        raise ValueError(f"Time step {dt} violates Nyquist criterion")

    # Numerical precision constraints
    if dt < 1e-6:
        raise ValueError("Time step too small, numerical precision issues")

    return True