# Example from: docs\api\simulation_engine_api_reference.md
# Index: 6
# Runnable: False
# Hash: 70936b74

# example-metadata:
# runnable: false

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
    **_kwargs: Any,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate a single controller trajectory using explicit Euler method."""