# Example from: docs\guides\api\simulation.md
# Index: 26
# Runnable: True
# Hash: c822c41e

# Coarse timestep for prototyping (faster)
config.simulation.dt = 0.01  # 10ms
runner = SimulationRunner(config)

# Fine timestep for accuracy (slower)
config.simulation.dt = 0.001  # 1ms
runner_accurate = SimulationRunner(config)

# Adaptive timestep (future feature)
# runner = SimulationRunner(config, adaptive_dt=True, dt_min=0.0001, dt_max=0.01)