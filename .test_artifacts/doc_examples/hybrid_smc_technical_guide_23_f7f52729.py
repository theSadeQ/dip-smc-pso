# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 23
# Runnable: False
# Hash: f7f52729

# example-metadata:
# runnable: false

def validate_hybrid_parameters(gains, config):
    """Validate hybrid controller parameters for stability."""

    c1, lambda1, c2, lambda2 = gains

    checks = {
        'positive_gains': all(g > 0 for g in [c1, lambda1, c2, lambda2]),
        'reasonable_ratios': c1/lambda1 > 0.5 and c2/lambda2 > 0.5,
        'adaptation_bounds': config.k1_max > config.k1_init * 5,
        'dead_zone_valid': config.dead_zone <= config.sat_soft_width,
    }

    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        raise ValueError(f"Parameter validation failed: {failed}")

    return True