# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 5
# Runnable: False
# Hash: 7e2c26b9

# example-metadata:
# runnable: false

def update_adaptive_gain(sigma, prev_K, dt):
    """Update K with dead zone, leak, and rate limiting."""

    # Dead zone logic
    if abs(sigma) <= self.dead_zone:
        dK = 0.0  # Freeze adaptation inside dead zone
    else:
        # Outside dead zone: growth with leak
        growth = self.gamma * abs(sigma)
        dK = growth - self.leak_rate * (prev_K - self.K_init)

    # Rate limiting
    dK = np.clip(dK, -self.adapt_rate_limit, self.adapt_rate_limit)

    # Update with bounds
    new_K = prev_K + dK * dt
    new_K = np.clip(new_K, self.K_min, self.K_max)

    return new_K, dK