# Example from: docs\guides\api\plant-models.md
# Index: 11
# Runnable: False
# Hash: 08deecd3

# example-metadata:
# runnable: false

# Optimize with simplified dynamics (fast)
config.simulation.use_full_dynamics = False
dynamics_simple = SimplifiedDynamics(config.dip_params)
runner_simple = SimulationRunner(config, dynamics_model=dynamics_simple)

tuner = PSOTuner(SMCType.CLASSICAL, bounds, config=config)
best_gains, _ = tuner.optimize()

# Validate with full dynamics (accurate)
config.simulation.use_full_dynamics = True
dynamics_full = FullDynamics(config.dip_params)
runner_full = SimulationRunner(config, dynamics_model=dynamics_full)

controller = create_smc_for_pso(SMCType.CLASSICAL, best_gains)
result = runner_full.run(controller)

print(f"Validation ISE: {result['metrics']['ise']:.4f}")