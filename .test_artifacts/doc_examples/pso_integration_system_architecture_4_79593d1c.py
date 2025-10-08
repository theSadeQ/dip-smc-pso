# Example from: docs\pso_integration_system_architecture.md
# Index: 4
# Runnable: True
# Hash: 79593d1c

def _compute_cost_from_traj(self, t, x_b, u_b, sigma_b) -> np.ndarray:
    """
    Multi-stage cost computation:
    1. Detect instability (angle limits, trajectory explosion)
    2. Compute time-mask for early termination
    3. Integrate weighted cost components
    4. Apply graded penalties for failure
    5. Normalize by baseline performance constants
    """