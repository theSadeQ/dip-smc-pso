# Example from: docs\guides\api\optimization.md
# Index: 23
# Runnable: True
# Hash: 8353eb78

# Problem complexity vs swarm size
problem_dimensions = len(bounds)

if problem_dimensions <= 4:
    n_particles = 20  # Hybrid controller (4 gains)
elif problem_dimensions <= 6:
    n_particles = 30  # Classical/STA (6 gains)
else:
    n_particles = 50  # Complex problems