# Example from: docs\technical\mathematical_foundations.md
# Index: 3
# Runnable: False
# Hash: 7cc4b928

# example-metadata:
# runnable: false

def validate_adaptive_smc_parameters(config):
    """Validate adaptive SMC parameters for stability."""

    # Surface gains validation
    validate_surface_gains(config.gains[:4])

    # Adaptation rate validation
    gamma = config.gains[4]  # Adaptation rate
    assert 0 < gamma < 10.0, "Adaptation rate must be in (0, 10) for stability"

    # Parameter bounds validation
    assert hasattr(config, 'K_min') and hasattr(config, 'K_max')
    assert 0 < config.K_min < config.K_max, "Parameter bounds must satisfy 0 < K_min < K_max"

    # Dead zone validation
    assert config.dead_zone > 0, "Dead zone must be positive to prevent parameter drift"