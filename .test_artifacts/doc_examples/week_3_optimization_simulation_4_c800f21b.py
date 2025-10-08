# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 4
# Runnable: True
# Hash: c800f21b

# Inertia term
velocity = self.inertia * velocity

# Cognitive component (personal best attraction)
cognitive = self.c1 * rand(0,1) * (pbest - position)
velocity += cognitive

# Social component (global best attraction)
social = self.c2 * rand(0,1) * (gbest - position)
velocity += social