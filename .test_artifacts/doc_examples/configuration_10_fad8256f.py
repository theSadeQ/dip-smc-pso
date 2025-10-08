# Example from: docs\guides\api\configuration.md
# Index: 10
# Runnable: True
# Hash: fad8256f

# Load base config
base_config = load_config('config.yaml')

# Override specific parameters
base_config.simulation.duration = 10.0  # Run for 10 seconds
base_config.simulation.use_full_dynamics = True  # Use full dynamics
base_config.dip_params.m1 = 0.75  # Increase first pendulum mass

# Use modified config
runner = SimulationRunner(base_config)