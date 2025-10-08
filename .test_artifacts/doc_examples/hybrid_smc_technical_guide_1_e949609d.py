# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 1
# Runnable: False
# Hash: e949609d

class HybridAdaptiveSTASMC:
    """
    Modular hybrid controller with clear separation of concerns:

    Components:
    - Sliding surface computation (absolute/relative modes)
    - Adaptive gain management (with anti-windup)
    - Super-twisting control law (finite-time convergent)
    - Equivalent control (model-based feedforward)
    - Cart recentering (with hysteresis)
    """