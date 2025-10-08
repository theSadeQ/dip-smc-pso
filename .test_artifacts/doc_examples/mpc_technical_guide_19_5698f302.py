# Example from: docs\controllers\mpc_technical_guide.md
# Index: 19
# Runnable: False
# Hash: 5698f302

# example-metadata:
# runnable: false

weights = MPCWeights(
    q_x=0.5,          # Less emphasis on cart position
    q_theta=20.0,     # Strong angle penalty
    q_xdot=0.05,
    q_thetadot=1.0,   # Higher damping
    r_u=5e-3          # Allow aggressive control
)

mpc = MPCController(
    dynamics_model=dynamics,
    horizon=30,                     # Long horizon
    dt=0.01,                        # Fine timestep
    weights=weights,
    max_force=50.0,                 # Higher force limit
    use_exact_discretization=True
)