# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 24
# Runnable: False
# Hash: ee16d41b

# example-metadata:
# runnable: false

# Development: Permissive limits for debugging
states_dev = simulate(x0, u, dt, energy_limits=1e6, state_bounds=(None, None))

# Production: Strict limits for safety
states_prod = simulate(
    x0, u, dt,
    energy_limits=100.0,
    state_bounds=(
        [-10.0, -np.pi, -np.pi, -50.0, -50.0, -50.0],
        [ 10.0,  np.pi,  np.pi,  50.0,  50.0,  50.0]
    )
)