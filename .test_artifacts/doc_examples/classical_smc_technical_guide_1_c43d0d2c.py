# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 1
# Runnable: True
# Hash: c43d0d2c

class ClassicalSMC:
    """
    Classical Sliding-Mode Controller with modular design:

    Components:
    - Sliding surface computation (linear combination)
    - Equivalent control (model-based feedforward)
    - Robust switching term (chattering reduction)
    - Saturation and safety mechanisms
    """