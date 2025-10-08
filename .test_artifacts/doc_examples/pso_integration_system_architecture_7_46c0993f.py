# Example from: docs\pso_integration_system_architecture.md
# Index: 7
# Runnable: True
# Hash: 46c0993f

# Typical performance characteristics:
PARTICLES = 50
ITERATIONS = 100
SIMULATION_TIME = 10.0  # seconds
DT = 0.001             # seconds

# Expected performance:
ITERATION_TIME = 0.8    # seconds per iteration
TOTAL_OPTIMIZATION = 80  # seconds for full PSO run
MEMORY_USAGE = 200      # MB peak memory