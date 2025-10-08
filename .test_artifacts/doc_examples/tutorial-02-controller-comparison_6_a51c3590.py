# Example from: docs\guides\tutorials\tutorial-02-controller-comparison.md
# Index: 6
# Runnable: True
# Hash: a51c3590

from controllers import get_gain_bounds_for_pso, SMCType
   bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
   print("Recommended gain bounds:", bounds)