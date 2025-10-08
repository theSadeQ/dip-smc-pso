# Example from: docs\guides\api\simulation.md
# Index: 12
# Runnable: True
# Hash: fedf5487

# Create custom dynamics
custom_dynamics = FrictionEnhancedDynamics(config.dip_params, friction_model='coulomb')

# Use with simulation runner
runner = SimulationRunner(config, dynamics_model=custom_dynamics)
result = runner.run(controller)