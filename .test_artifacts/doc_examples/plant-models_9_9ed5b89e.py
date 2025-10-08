# Example from: docs\guides\api\plant-models.md
# Index: 9
# Runnable: True
# Hash: 9ed5b89e

# Create custom dynamics
custom_dynamics = CoulombFrictionDynamics(config.dip_params, mu_coulomb=0.3)

# Use with simulation runner
runner = SimulationRunner(config, dynamics_model=custom_dynamics)
result = runner.run(controller)

print(f"ISE with Coulomb friction: {result['metrics']['ise']:.4f}")