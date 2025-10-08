# Example from: docs\controllers\factory_system_guide.md
# Index: 9
# Runnable: False
# Hash: ccd017c6

# example-metadata:
# runnable: false

def _validate_controller_gains(gains, controller_info, controller_type):
    """Validate controller gains with controller-specific rules."""

    # 1. Count validation
    if len(gains) != controller_info['gain_count']:
        raise ValueError(f"Expected {controller_info['gain_count']} gains, got {len(gains)}")

    # 2. Finite values
    if not all(isinstance(g, (int, float)) and np.isfinite(g) for g in gains):
        raise ValueError("All gains must be finite numbers")

    # 3. Positivity
    if any(g <= 0 for g in gains):
        raise ValueError("All gains must be positive")

    # 4. Controller-specific constraints
    if controller_type == 'sta_smc' and len(gains) >= 2:
        K1, K2 = gains[0], gains[1]
        if K1 <= K2:
            raise ValueError("Super-Twisting stability requires K1 > K2 > 0")