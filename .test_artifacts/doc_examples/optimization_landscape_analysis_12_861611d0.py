# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 12
# Runnable: True
# Hash: 861611d0

if violation_rate > 0.2:  # 20% of particles violate
    mu *= 1.5  # Increase penalty
elif violation_rate < 0.05:
    mu *= 0.9  # Decrease penalty (may be too conservative)