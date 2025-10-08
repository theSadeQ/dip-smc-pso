# Example from: docs\benchmarks\controller_performance_benchmarks.md
# Index: 2
# Runnable: True
# Hash: cda12e3d

from src.plant.configurations import DIPConfig

# Initialize dynamics with config
config = DIPConfig()  # Uses default parameters
dynamics = SimplifiedDIPDynamics(config=config)