# Example from: docs\optimization_simulation\guide.md
# Index: 29
# Runnable: False
# Hash: d498ed85

def run_simulation(
    *,
    controller: Any,
    dynamics_model: Any,
    sim_time: float,
    dt: float,
    initial_state: Any,
    u_max: Optional[float] = None,
    seed: Optional[int] = None,
    rng: Optional[np.random.Generator] = None,
    latency_margin: Optional[float] = None,
    fallback_controller: Optional[Callable[[float, np.ndarray], float]] = None,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Simulate single controller trajectory using Euler integration.

    Parameters
    ----------
    controller : Any
        Controller object (compute_control or __call__ interface)
    dynamics_model : Any
        Dynamics model with step(state, u, dt) method
    sim_time : float
        Total simulation duration (seconds)
    dt : float
        Integration timestep (seconds), must be > 0
    initial_state : array-like
        Initial state vector
    u_max : float, optional
        Control saturation limit
    fallback_controller : callable, optional
        Fallback controller for deadline misses

    Returns
    -------
    t_arr : np.ndarray, shape (N+1,)
        Time vector
    x_arr : np.ndarray, shape (N+1, D)
        State trajectory
    u_arr : np.ndarray, shape (N,)
        Control sequence
    """