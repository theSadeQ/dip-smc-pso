# Example from: docs\guides\api\simulation.md
# Index: 25
# Runnable: False
# Hash: 97939488

# example-metadata:
# runnable: false

# PSO optimization: Use simplified dynamics for speed
config.simulation.use_full_dynamics = False
runner = SimulationRunner(config)
tuner = PSOTuner(..., simulation_runner=runner)
best_gains = tuner.optimize()  # Fast iterations

# Final validation: Use full dynamics for accuracy
config.simulation.use_full_dynamics = True
runner = SimulationRunner(config)
controller = create_smc_for_pso(SMCType.CLASSICAL, best_gains)
final_result = runner.run(controller)  # Accurate validation