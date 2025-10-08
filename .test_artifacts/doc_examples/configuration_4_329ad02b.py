# Example from: docs\guides\api\configuration.md
# Index: 4
# Runnable: True
# Hash: 329ad02b

# Load different configs for different scenarios
config_baseline = load_config('config.yaml')
config_challenging = load_config('config_challenging.yaml')
config_hil = load_config('config_hil.yaml')

# Use appropriate config for each scenario
if scenario == 'baseline':
    runner = SimulationRunner(config_baseline)
elif scenario == 'challenging':
    runner = SimulationRunner(config_challenging)