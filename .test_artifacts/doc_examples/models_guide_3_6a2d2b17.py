# Example from: docs\plant\models_guide.md
# Index: 3
# Runnable: True
# Hash: 6a2d2b17

from src.plant.models.simplified import SimplifiedDIPDynamics, SimplifiedDIPConfig

# Create configuration
config = SimplifiedDIPConfig.create_default()

# Initialize dynamics model
dynamics = SimplifiedDIPDynamics(
    config=config,
    enable_fast_mode=True,      # Use Numba JIT compilation
    enable_monitoring=True       # Track performance metrics
)

# Compute dynamics
state = np.array([0.1, 0.05, -0.03, 0.0, 0.0, 0.0])
control = np.array([5.0])

result = dynamics.compute_dynamics(state, control)

if result.success:
    state_derivative = result.state_derivative
    energy = result.info['total_energy']
    print(f"Energy: {energy:.4f} J")
else:
    print(f"Error: {result.info['failure_reason']}")