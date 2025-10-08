# Example from: docs\controllers\mpc_technical_guide.md
# Index: 20
# Runnable: False
# Hash: 855f78a3

weights = MPCWeights(
    q_theta=10.0,
    r_u=1e-2
)

mpc = MPCController(
    dynamics_model=dynamics,
    horizon=12,                     # Shorter horizon
    dt=0.02,                        # Standard timestep
    weights=weights,
    max_force=20.0,
    use_exact_discretization=False, # Faster Euler
    max_du=15.0                     # Slew rate limit
)