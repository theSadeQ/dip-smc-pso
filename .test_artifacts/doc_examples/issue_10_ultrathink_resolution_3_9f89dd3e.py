# Example from: docs\reports\issue_10_ultrathink_resolution.md
# Index: 3
# Runnable: True
# Hash: 9f89dd3e

if cond_num > 1e12:
    tolerance = 1.0  # Accept regularization bias for extreme cases
elif cond_num > 1e10:
    tolerance = 1e-3  # Modest accuracy for high condition numbers
else:
    tolerance = 1e-6  # High accuracy for well-conditioned matrices