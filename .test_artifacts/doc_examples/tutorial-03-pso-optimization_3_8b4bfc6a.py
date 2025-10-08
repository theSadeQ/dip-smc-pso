# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 3
# Runnable: True
# Hash: 8b4bfc6a

import json

baseline = json.load(open('baseline_classical.json'))
optimized = json.load(open('optimized_classical_results.json'))

print("Performance Improvement:")
print(f"ISE:        {baseline['metrics']['ise']:.4f} → {optimized['metrics']['ise']:.4f} "
      f"({(1 - optimized['metrics']['ise']/baseline['metrics']['ise'])*100:.1f}% better)")
print(f"Settling:   {baseline['metrics']['settling_time']:.2f}s → {optimized['metrics']['settling_time']:.2f}s")
print(f"Overshoot:  {baseline['metrics']['overshoot']:.2f}% → {optimized['metrics']['overshoot']:.2f}%")