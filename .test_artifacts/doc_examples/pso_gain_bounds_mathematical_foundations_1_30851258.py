# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 1
# Runnable: True
# Hash: 30851258

def validate_sta_damping(lambda1, lambda2):
    """Validate STA surface coefficients for Issue #2 compliance."""
    damping_ratio = lambda2 / (2 * np.sqrt(lambda1))
    natural_freq = np.sqrt(lambda1)

    # Issue #2 compliance checks
    damping_ok = 0.6 <= damping_ratio <= 0.8  # Avoid underdamping
    frequency_ok = 0.3 <= natural_freq <= 3.2  # Physical realizability
    overshoot_ok = damping_ratio >= 0.69       # <5% overshoot guarantee

    return damping_ok and frequency_ok and overshoot_ok