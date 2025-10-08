# Example from: docs\api\factory_system_api_reference.md
# Index: 30
# Runnable: True
# Hash: d17342b3

from src.controllers.factory import SMCType, create_smc_for_pso

# PSO creates controller for each particle
particle_gains = [20.5, 14.3, 11.8, 9.2, 38.1, 5.7]
controller_wrapper = create_smc_for_pso(
    smc_type=SMCType.CLASSICAL,
    gains=particle_gains,
    max_force=150.0,
    dt=0.001
)

# Wrapper exposes PSO attributes
print(f"Expected gains: {controller_wrapper.n_gains}")  # 6
print(f"Controller type: {controller_wrapper.controller_type}")  # 'classical_smc'

# Use in PSO fitness function
state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])
control = controller_wrapper.compute_control(state)