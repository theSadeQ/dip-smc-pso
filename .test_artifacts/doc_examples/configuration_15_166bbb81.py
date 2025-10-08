# Example from: docs\guides\api\configuration.md
# Index: 15
# Runnable: False
# Hash: 166bbb81

# development.yaml
simulation:
  duration: 2.0              # Shorter for faster iteration
  dt: 0.01
  use_full_dynamics: false   # Simplified for speed

pso:
  n_particles: 20            # Smaller swarm for speed
  iters: 50

# production.yaml
simulation:
  duration: 10.0             # Full simulation
  dt: 0.001                  # Fine timestep for accuracy
  use_full_dynamics: true    # Full nonlinear dynamics

pso:
  n_particles: 50            # Larger swarm for better results
  iters: 200