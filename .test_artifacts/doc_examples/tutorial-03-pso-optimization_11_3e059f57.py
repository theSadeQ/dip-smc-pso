# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 11
# Runnable: True
# Hash: 3e059f57

if max(abs(state)) > 10.0:  # Detect divergence
       return float('inf')     # Penalize heavily