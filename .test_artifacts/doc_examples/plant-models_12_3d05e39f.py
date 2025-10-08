# Example from: docs\guides\api\plant-models.md
# Index: 12
# Runnable: False
# Hash: 3d05e39f

# Compare simplified vs full dynamics
results_comparison = {}

for model_name, dynamics in [
    ('Simplified', SimplifiedDynamics(config.dip_params)),
    ('Full', FullDynamics(config.dip_params))
]:
    runner = SimulationRunner(config, dynamics_model=dynamics)
    result = runner.run(controller)
    results_comparison[model_name] = result

# Analyze differences
for model, result in results_comparison.items():
    print(f"{model}: ISE={result['metrics']['ise']:.4f}, "
          f"Settling={result['metrics']['settling_time']:.2f}s")