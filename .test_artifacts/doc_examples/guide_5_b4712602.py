# Example from: docs\optimization_simulation\guide.md
# Index: 5
# Runnable: False
# Hash: b4712602

# example-metadata:
# runnable: false

def simulate_system_batch(
    *,
    controller_factory: Callable[[np.ndarray], Any],
    particles: np.ndarray,          # Shape: (B, G) for B particles, G gains
    sim_time: float,
    dt: float,
    u_max: Optional[float] = None,
    params_list: Optional[List] = None,  # Uncertainty evaluation
    convergence_tol: Optional[float] = None,  # Early stopping threshold
    grace_period: float = 0.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns:
    -------
    t : np.ndarray, shape (N+1,)
        Time vector
    x_b : np.ndarray, shape (B, N+1, D)
        State trajectories for B particles
    u_b : np.ndarray, shape (B, N)
        Control sequences
    sigma_b : np.ndarray, shape (B, N)
        Sliding surface values
    """