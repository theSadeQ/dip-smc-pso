# Example from: docs\optimization_simulation\guide.md
# Index: 17
# Runnable: True
# Hash: 535afd22

# High accuracy (slow)
config.simulation.dt = 0.001  # 1 ms timestep

# Balanced (recommended)
config.simulation.dt = 0.01   # 10 ms timestep

# Fast prototyping (low accuracy)
config.simulation.dt = 0.05   # 50 ms timestep