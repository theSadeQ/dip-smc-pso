# Example from: docs\PSO_Documentation_Validation_Report.md
# Index: 3
# Runnable: False
# Hash: 29aaca78

def _compute_cost_from_traj(
    self, t: np.ndarray, x_b: np.ndarray, u_b: np.ndarray, sigma_b: np.ndarray
) -> np.ndarray:
    """Compute the cost per particle from simulated trajectories.

    The cost combines state error, control effort, control slew and a
    sliding-mode stability term.  State error integrates the squared
    deviation of all state components over the horizon.  Control terms
    integrate squared commands and their rates.  A graded instability
    penalty is applied when trajectories fail early.
    """