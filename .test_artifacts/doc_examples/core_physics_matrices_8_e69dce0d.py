# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 8
# Runnable: True
# Hash: e69dce0d

from src.plant.models.full import FullDIPDynamics

# Create full dynamics model (uses DIPPhysicsMatrices internally)
dynamics = FullDIPDynamics(config)

# Simulate one timestep
control_input = np.array([5.0])  # 5N force on cart
result = dynamics.compute_dynamics(state, control_input, time=0.0)

if result.success:
    state_derivative = result.state_derivative
    print(f"State derivative: {state_derivative}")

    # Access physics matrices from dynamics model
    M, C, G = dynamics.get_physics_matrices(state)