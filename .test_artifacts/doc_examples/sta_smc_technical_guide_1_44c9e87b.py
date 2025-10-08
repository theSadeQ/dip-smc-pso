# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 1
# Runnable: False
# Hash: 44c9e87b

class SuperTwistingSMC:
    """
    Second-order sliding mode controller (STA):

    Components:
    - Sliding surface computation (same as adaptive)
    - Super-twisting continuous term (√|σ|)
    - Integral term update (discontinuous derivative)
    - Equivalent control (optional, model-based)
    - Numba acceleration for performance
    """