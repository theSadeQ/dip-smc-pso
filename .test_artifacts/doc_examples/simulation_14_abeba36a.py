# Example from: docs\guides\api\simulation.md
# Index: 14
# Runnable: True
# Hash: abeba36a

# Automatic instability detection
if context.is_numerically_unstable(state):
    print("Warning: Numerical instability detected")
    context.attempt_recovery()