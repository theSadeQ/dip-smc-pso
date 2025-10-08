# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 3
# Runnable: True
# Hash: 7e53b394

if gains[0] <= gains[1]:  # K1 <= K2
    penalty = 1e6 * (gains[1] - gains[0] + 1)