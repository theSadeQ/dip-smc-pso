# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 8
# Runnable: True
# Hash: 024f4401

class ModularSuperTwistingSMC:
    """Modular super-twisting sliding mode control wrapper.

    Wraps SuperTwistingSMC (2nd-order sliding mode) for factory integration.
    Provides chattering reduction through continuous control law.

    See Also
    --------
    SuperTwistingSMC : Implementation in src/controllers/sta_smc.py
    """