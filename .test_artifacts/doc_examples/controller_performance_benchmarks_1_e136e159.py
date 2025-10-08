# Example from: docs\benchmarks\controller_performance_benchmarks.md
# Index: 1
# Runnable: True
# Hash: e136e159

# Old API (used in benchmark script)
dynamics = SimplifiedDIPDynamics()

# New API (required after refactoring)
from src.plant.configurations import DIPConfig
dynamics = SimplifiedDIPDynamics(config=DIPConfig())