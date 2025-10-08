# Example from: docs\optimization_simulation\guide.md
# Index: 30
# Runnable: False
# Hash: ea23d68b

def simulate_system_batch(
    *,
    controller_factory: Callable[[np.ndarray], Any],
    particles: np.ndarray,
    sim_time: float,
    dt: float,
    u_max: Optional[float] = None,
    params_list: Optional[List] = None,
    convergence_tol: Optional[float] = None,
    grace_period: float = 0.0,
    **kwargs
) -> Union[
    Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]
]:
    """
    Vectorized batch simulation of multiple controllers.

    Parameters
    ----------
    controller_factory : callable
        Factory function: controller = factory(gains)
    particles : np.ndarray, shape (B, G)
        Gain vectors for B particles
    sim_time : float
        Total simulation duration
    dt : float
        Integration timestep
    u_max : float, optional
        Control saturation limit
    params_list : list, optional
        List of physics parameter objects for uncertainty evaluation
    convergence_tol : float, optional
        Early stopping threshold for max(|σ|)
    grace_period : float
        Duration before convergence checking begins

    Returns
    -------
    If params_list is None:
        (t, x_batch, u_batch, sigma_batch)
    If params_list is provided:
        List of (t, x_batch, u_batch, sigma_batch) tuples

    Notes
    -----
    - t: shape (N+1,)
    - x_batch: shape (B, N+1, D)
    - u_batch: shape (B, N)
    - sigma_batch: shape (B, N)
    """