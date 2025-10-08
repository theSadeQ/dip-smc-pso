# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 10
# Runnable: True
# Hash: 1b8368ef

def penalty_k1_k2(gains, penalty_weight=1000):
    """Penalty for K1 <= K2 violation."""
    if gains[0] <= gains[1]:
        violation = gains[1] - gains[0] + 0.1  # Margin
        return penalty_weight * violation**2
    return 0.0