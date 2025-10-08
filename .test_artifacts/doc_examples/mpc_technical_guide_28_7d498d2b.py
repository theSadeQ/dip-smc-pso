# Example from: docs\controllers\mpc_technical_guide.md
# Index: 28
# Runnable: True
# Hash: 7d498d2b

from src.optimization.algorithms.pso_optimizer import PSOTuner

def mpc_factory_for_pso(params):
    """
    params = [q_x, q_theta, q_xdot, q_thetadot, r_u, horizon]
    """
    weights = MPCWeights(
        q_x=params[0],
        q_theta=params[1],
        q_xdot=params[2],
        q_thetadot=params[3],
        r_u=params[4]
    )

    return MPCController(
        dynamics_model=dynamics,
        horizon=int(params[5]),
        dt=0.02,
        weights=weights
    )

# PSO bounds
bounds = [
    (0.1, 10.0),    # q_x
    (1.0, 50.0),    # q_theta
    (0.01, 1.0),    # q_xdot
    (0.1, 2.0),     # q_thetadot
    (1e-3, 0.1),    # r_u
    (10, 30)        # horizon (integer)
]

tuner = PSOTuner(
    controller_factory=mpc_factory_for_pso,
    config=config,
    bounds=bounds,
    n_particles=20,
    max_iters=50
)

result = tuner.optimise()
optimal_params = result['best_pos']