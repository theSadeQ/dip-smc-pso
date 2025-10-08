# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 3
# Runnable: True
# Hash: 9fe44e82

# Uncovered: Edge case validation
   if abs(sliding_surface) < 1e-12:  # ← Edge case not tested
       return 0.0