# Example from: docs\reference\controllers\smc_core_equivalent_control.md
# Index: 1
# Runnable: True
# Hash: 423f9923

from src.controllers.smc.core.equivalent_control import EquivalentControl
from src.plant.models.simplified import SimplifiedDIPDynamics

# Initialize dynamics model
dynamics = SimplifiedDIPDynamics()

# Initialize equivalent control module
eq_control = EquivalentControl(
    dynamics_model=dynamics,
    surface_gains=[10.0, 8.0, 15.0, 12.0]  # λ1, c1, λ2, c2
)

# Compute equivalent control for current state
state = np.array([0.1, 0.0, 0.05, 0.1, 0.02, 0.05])
u_eq = eq_control.compute(state)
print(f"Equivalent control: {u_eq:.2f} N")