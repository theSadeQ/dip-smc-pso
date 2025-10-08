# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 22
# Runnable: False
# Hash: 20a421eb

# example-metadata:
# runnable: false

def validate_classical_parameters(gains, config):
    """Validate classical SMC parameters for stability."""

    k1, k2, lam1, lam2, K, kd = gains

    checks = {
        'positive_gains': all(g > 0 for g in [k1, k2, lam1, lam2, K]),
        'nonneg_damping': kd >= 0,
        'hurwitz_1': k1**2 >= 4*lam1,  # Critically damped or overdamped
        'hurwitz_2': k2**2 >= 4*lam2,
        'switching_adequate': K > 20,  # Typical disturbance bound
        'boundary_positive': config.boundary_layer > 0,
    }

    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        print(f"WARNING: Parameter validation failed: {failed}")
        return False

    return True