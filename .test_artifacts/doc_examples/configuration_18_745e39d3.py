# Example from: docs\guides\api\configuration.md
# Index: 18
# Runnable: True
# Hash: 745e39d3

scenarios = ['baseline', 'challenging', 'extreme']
results = {}

for scenario in scenarios:
    config = load_config(f'scenarios/{scenario}.yaml')
    runner = SimulationRunner(config)
    results[scenario] = runner.run(controller)