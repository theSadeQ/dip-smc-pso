# Example from: docs\numerical_stability_guide.md
# Index: 4
# Runnable: True
# Hash: 4c76aa7a

if sv_ratio < 1e-8:
    reg_scale = alpha * s[0] * 1e4