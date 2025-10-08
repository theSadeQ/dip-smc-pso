# Example from: docs\theory\numerical_stability_methods.md
# Index: 13
# Runnable: False
# Hash: 8ff3f2cb

# example-metadata:
# runnable: false

from src.plant.core.numerical_stability import NumericalStabilityMonitor
monitor = NumericalStabilityMonitor()
# ... during simulation ...
stats = monitor.get_statistics()
print(f"Regularization rate: {stats['regularization_rate']:.2%}")