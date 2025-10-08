# Example from: docs\pso_integration_system_architecture.md
# Index: 3
# Runnable: False
# Hash: d47e96af

def simulate_system_batch(
    controller_factory: Callable,
    particles: np.ndarray,
    sim_time: float,
    dt: float,
    u_max: float,
    params_list: Optional[List[DIPParams]] = None
) -> Union[Tuple, List[Tuple]]:
    """
    High-performance batch simulation architecture:

    Performance Features:
    - Vectorized integration (Numba-optimized)
    - Memory-efficient trajectory storage
    - Parallel controller evaluation
    - Early termination for unstable trajectories

    Returns:
    - Time vectors: t ∈ ℝᵀ
    - State trajectories: x ∈ ℝᴮˣᵀˣ⁶
    - Control trajectories: u ∈ ℝᴮˣᵀ
    - Sliding variables: σ ∈ ℝᴮˣᵀ
    """