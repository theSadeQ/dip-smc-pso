# Example from: docs\controllers\factory_system_guide.md
# Index: 17
# Runnable: False
# Hash: 571350a9

# example-metadata:
# runnable: false

def validate_smc_gains(smc_type: SMCType, gains: np.ndarray) -> bool:
    """Validate gains for PSO particle evaluation."""

    spec = SMC_GAIN_SPECS[smc_type]

    # Check length
    if len(gains) != spec.n_gains:
        return False

    # Check positivity for surface gains
    if any(g <= 0 for g in gains[:4]):
        return False

    # Controller-specific constraints
    if smc_type == SMCType.SUPER_TWISTING:
        K1, K2 = gains[0], gains[1]
        if K1 <= K2:  # Stability requirement
            return False

    return True