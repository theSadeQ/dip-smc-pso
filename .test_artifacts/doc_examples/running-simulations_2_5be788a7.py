# Example from: docs\guides\how-to\running-simulations.md
# Index: 2
# Runnable: True
# Hash: 5be788a7

from src.controllers.factory import create_controller
from src.core.simulation_runner import SimulationRunner
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller(
    'classical_smc',
    config=config.controllers.classical_smc
)

# Initialize simulation runner
runner = SimulationRunner(config)

# Run simulation
result = runner.run(controller)

# Access results
print(f"ISE: {result['metrics']['ise']:.4f}")
print(f"Settling Time: {result['metrics']['settling_time']:.2f}s")

# Access trajectories
import numpy as np
time = np.array(result['time'])
state = np.array(result['state'])
control = np.array(result['control'])

# Extract specific states
theta1 = state[:, 2]  # First pendulum angle
theta2 = state[:, 4]  # Second pendulum angle