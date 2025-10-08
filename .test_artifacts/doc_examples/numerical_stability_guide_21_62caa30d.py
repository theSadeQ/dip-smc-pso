# Example from: docs\numerical_stability_guide.md
# Index: 21
# Runnable: False
# Hash: 62caa30d

# Track regularization in production
from src.plant.core.numerical_stability import NumericalStabilityMonitor

monitor = NumericalStabilityMonitor()
# ... run simulations ...
stats = monitor.get_statistics()
if stats['regularization_rate'] > 0.5:
    warnings.warn("High regularization frequency detected")