# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 15
# Runnable: True
# Hash: 7b627c86

# Override config defaults
states = simulate(
    x0, u, dt,
    energy_limits=200.0,  # More permissive than config
    state_bounds=(None, None)  # Disable bounds checking
)