# Example from: docs\api\factory_methods_reference.md
# Index: 15
# Runnable: True
# Hash: 6d6513b0

from src.controllers.factory import create_smc_for_pso, SMCType

# Create PSO-compatible controller
gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=gains,
    max_force=150.0,
    dt=0.001
)

# Use in PSO fitness function
def fitness_function(test_gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, test_gains)
    return evaluate_controller_performance(controller)

# Validate particle swarm
particles = np.array([
    [20, 15, 12, 8, 35, 5],
    [25, 20, 15, 10, 40, 6],
    [0, 0, 0, 0, 0, 0]  # Invalid
])
validity = controller.validate_gains(particles)
print(f"Particle validity: {validity}")
# Output: [True, True, False]