# Example from: docs\guides\api\simulation.md
# Index: 22
# Runnable: True
# Hash: b99d4cb3

from src.config import load_config
from src.controllers import create_controller
from src.core import SimulationRunner
from src.utils.visualization import plot_results

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller('classical_smc', config=config.controllers.classical_smc)

# Initialize simulation
runner = SimulationRunner(config)

# Run simulation
result = runner.run(controller)

# Visualize
plot_results(result)

# Analyze
print(f"Performance Metrics:")
print(f"  ISE: {result['metrics']['ise']:.4f}")
print(f"  Settling Time: {result['metrics']['settling_time']:.2f}s")
print(f"  Max θ₁: {result['metrics']['max_theta1']:.3f} rad")