# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 14
# Runnable: True
# Hash: ffdeb0fa

# Example 1: Method comparison
from benchmarks import IntegrationBenchmark

benchmark = IntegrationBenchmark()
results = benchmark.comprehensive_comparison()

for method, metrics in results.items():
    print(f"{method}:")
    print(f"  Convergence order: {metrics['convergence_order']:.2f}")
    print(f"  Energy drift: {metrics['energy_drift']:.2e}")
    print(f"  Computation time: {metrics['computation_time']:.3f}s")

# Example 2: Energy conservation validation
conservation = benchmark.validate_conservation_laws()
print(f"Max energy drift: {conservation['max_drift']:.2e}")