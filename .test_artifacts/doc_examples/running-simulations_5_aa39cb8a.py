# Example from: docs\guides\how-to\running-simulations.md
# Index: 5
# Runnable: True
# Hash: aa39cb8a

# In Jupyter notebook
%matplotlib inline
import matplotlib.pyplot as plt
from src.controllers.factory import create_controller
from src.core.simulation_runner import SimulationRunner
from src.config import load_config

# Load config
config = load_config('config.yaml')

# Run simulation
controller = create_controller('classical_smc', config=config.controllers.classical_smc)
runner = SimulationRunner(config)
result = runner.run(controller)

# Plot results inline
fig, axes = plt.subplots(3, 1, figsize=(12, 8))

time = result['time']
state = np.array(result['state'])
control = result['control']

# Pendulum angles
axes[0].plot(time, state[:, 2], label='θ₁')
axes[0].plot(time, state[:, 4], label='θ₂')
axes[0].set_ylabel('Angle (rad)')
axes[0].legend()
axes[0].grid()

# Angular velocities
axes[1].plot(time, state[:, 3], label='dθ₁')
axes[1].plot(time, state[:, 5], label='dθ₂')
axes[1].set_ylabel('Angular Velocity (rad/s)')
axes[1].legend()
axes[1].grid()

# Control signal
axes[2].plot(time, control)
axes[2].set_xlabel('Time (s)')
axes[2].set_ylabel('Control Force (N)')
axes[2].grid()

plt.tight_layout()
plt.show()

# Display metrics
print(f"ISE: {result['metrics']['ise']:.4f}")
print(f"Settling Time: {result['metrics']['settling_time']:.2f}s")