# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 11
# Runnable: True
# Hash: d662a48c

# Problematic: Exact floating-point comparison
   assert stability_margin == 0.5  # ← Can fail due to floating-point errors

   # Solution: Use tolerance-based comparison
   assert abs(stability_margin - 0.5) < 1e-6