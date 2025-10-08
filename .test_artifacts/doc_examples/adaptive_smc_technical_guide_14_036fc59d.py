# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 14
# Runnable: False
# Hash: 036fc59d

def validate_adaptive_parameters(gains, config):
    """Validate adaptive SMC parameters."""

    k1, k2, lam1, lam2, gamma = gains

    checks = {
        'positive_gains': all(g > 0 for g in [k1, k2, lam1, lam2, gamma]),
        'K_bounds_valid': config.K_min <= config.K_init <= config.K_max,
        'dead_zone_nonneg': config.dead_zone >= 0,
        'leak_rate_nonneg': config.leak_rate >= 0,
        'adapt_rate_positive': config.adapt_rate_limit > 0,
        'gamma_reasonable': 0.01 <= gamma <= 10.0,
    }

    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        print(f"WARNING: Parameter validation failed: {failed}")
        return False

    return True