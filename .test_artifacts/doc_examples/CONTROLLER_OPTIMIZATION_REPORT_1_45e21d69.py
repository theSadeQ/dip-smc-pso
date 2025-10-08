# Example from: docs\reports\CONTROLLER_OPTIMIZATION_REPORT.md
# Index: 1
# Runnable: True
# Hash: 45e21d69

# Before: No K1 > K2 validation
# After: Strict constraint enforcement
valid = (k1 > 0.0) & (k2 > 0.0) & (k1 > k2)