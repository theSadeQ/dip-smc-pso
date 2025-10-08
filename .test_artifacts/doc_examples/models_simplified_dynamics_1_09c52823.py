# Example from: docs\reference\plant\models_simplified_dynamics.md
# Index: 1
# Runnable: True
# Hash: 09c52823

from src.plant.models.simplified import SimplifiedDynamics
from src.plant.models.full import FullDynamics
from src.plant.configurations import DIPPhysicsConfig

# Simplified dynamics (fast, linearized friction)
simplified = SimplifiedDynamics(
    cart_mass=1.0,
    pole1_mass=0.1,
    pole2_mass=0.05,
    pole1_length=0.5,
    pole2_length=0.25,
    friction_cart=0.1
)

# Full nonlinear dynamics (high fidelity)
full = FullDynamics(
    config=DIPPhysicsConfig(
        cart_mass=1.0,
        pole1_mass=0.1,
        pole2_mass=0.05,
        pole1_length=0.5,
        pole2_length=0.25,
        friction_cart=0.1,
        friction_pole1=0.01,
        friction_pole2=0.01
    )
)

# Compute dynamics at a state
state = [0.1, 0.2, 0.1, 0, 0, 0]  # [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
control = 10.0

state_derivative = simplified.compute_dynamics(state, control, t=0)
print(f"Accelerations: {state_derivative[3:]}")  # [ẍ, θ̈₁, θ̈₂]