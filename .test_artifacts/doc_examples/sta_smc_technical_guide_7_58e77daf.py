# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 7
# Runnable: True
# Hash: 58e77daf

def validate_sta_gains(gains):
    """Ensure K1 > K2 for stability."""
    K1, K2 = gains[0], gains[1]
    if K1 <= K2:
        return False  # Invalid
    return True