# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 8
# Runnable: True
# Hash: 5d135371

from src.simulation.engines.vector_sim import simulate

# Pendulum with energy limit
states = simulate(
    x0,
    u,
    dt,
    energy_limits=100.0,  # Total energy < 100
    state_bounds=(
        [-10.0, -np.pi, -np.pi, -50.0, -50.0, -50.0],  # Lower bounds
        [ 10.0,  np.pi,  np.pi,  50.0,  50.0,  50.0]   # Upper bounds
    )
)