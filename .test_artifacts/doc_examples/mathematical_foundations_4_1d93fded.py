# Example from: docs\technical\mathematical_foundations.md
# Index: 4
# Runnable: False
# Hash: 1d93fded

# example-metadata:
# runnable: false

def validate_hybrid_smc_configuration(config):
    """Validate hybrid SMC configuration for stability."""

    # Validate sub-controller configurations
    assert hasattr(config, 'classical_config'), "Hybrid SMC requires classical sub-config"
    assert hasattr(config, 'adaptive_config'), "Hybrid SMC requires adaptive sub-config"

    validate_classical_smc_gains(config.classical_config.gains)
    validate_adaptive_smc_parameters(config.adaptive_config)

    # Validate switching logic parameters
    assert hasattr(config, 'hybrid_mode'), "Hybrid mode must be specified"
    assert config.dt > 0, "Timestep must be positive for switching logic"

    # Ensure dwell time constraint
    min_dwell_time = 0.001  # 1ms minimum
    assert config.dt >= min_dwell_time, f"Timestep must be ≥ {min_dwell_time}s for stability"