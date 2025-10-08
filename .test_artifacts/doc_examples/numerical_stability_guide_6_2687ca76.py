# Example from: docs\numerical_stability_guide.md
# Index: 6
# Runnable: True
# Hash: 2687ca76

if cond_num > 1e10:
    reg_scale = alpha * s[0] * 10