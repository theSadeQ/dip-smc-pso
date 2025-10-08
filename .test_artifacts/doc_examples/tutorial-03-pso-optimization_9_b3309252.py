# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 9
# Runnable: True
# Hash: b3309252

# Start with large swarm, reduce over time to save computation
initial_swarm = 50
final_swarm = 20

for iter in range(100):
    current_swarm_size = int(initial_swarm - (initial_swarm - final_swarm) * iter / 100)
    # Run PSO iteration with current_swarm_size