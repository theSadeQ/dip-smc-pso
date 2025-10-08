# Example from: docs\numerical_stability_guide.md
# Index: 19
# Runnable: True
# Hash: 583ecf6d

# Check regularization trigger frequency
monitor = NumericalStabilityMonitor()
stats = monitor.get_statistics()
print(f"Regularization rate: {stats['regularization_rate']:.1%}")