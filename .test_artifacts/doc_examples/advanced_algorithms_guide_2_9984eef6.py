# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 2
# Runnable: True
# Hash: 9984eef6

# Configure inertia weight schedule in config.yaml:
# pso:
#   w_schedule: [0.9, 0.4]  # Start at 0.9, end at 0.4
#   iters: 100
#   n_particles: 30

result = tuner.optimise()  # Uses w_schedule from config

# Manual iteration loop for custom control
from pyswarms.single import GlobalBestPSO

# Create optimizer
optimizer = GlobalBestPSO(
    n_particles=30,
    dimensions=6,
    options={'c1': 2.05, 'c2': 2.05, 'w': 0.9},
    bounds=(np.array([0.1]*6), np.array([50.0]*6))
)

# Inertia schedule
w_values = np.linspace(0.9, 0.4, 100)

for iteration, w_val in enumerate(w_values):
    optimizer.options['w'] = w_val
    step_cost, step_pos = optimizer.step(tuner._fitness)
    print(f"Iteration {iteration}: w={w_val:.3f}, cost={step_cost:.6f}")