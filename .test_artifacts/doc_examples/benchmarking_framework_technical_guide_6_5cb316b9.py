# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 6
# Runnable: False
# Hash: 5cb316b9

# src/benchmarks/core/trial_runner.py

def run_multiple_trials(controller_factory: Callable,
                       cfg: Any,
                       n_trials: int = 30,
                       seed: Optional[int] = None,
                       progress_callback: Optional[Callable] = None) -> List[dict]:
    """Execute multiple simulation trials with different random seeds.

    Implements Central Limit Theorem requirements (n ≥ 30) for statistical validity.

    Parameters
    ----------
    controller_factory : callable
        Function that returns a fresh controller instance
    cfg : object
        Configuration object with simulation parameters
    n_trials : int
        Number of trials (default: 30 for CLT compliance)
    seed : int, optional
        Base random seed for reproducibility
    progress_callback : callable, optional
        Callback function(current, total) for progress tracking

    Returns
    -------
    list of dict
        List of metric dictionaries, one per trial

    Examples
    --------
    >>> def create_controller():
    ...     return ClassicalSMC(gains=[10, 8, 15, 12, 50, 5], max_force=100)
    ...
    >>> metrics_list = run_multiple_trials(
    ...     create_controller, config, n_trials=30, seed=42,
    ...     progress_callback=lambda i, n: print(f"Trial {i}/{n}")
    ... )
    >>> ise_values = [m['ise'] for m in metrics_list]
    >>> mean_ise = np.mean(ise_values)
    """
    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()

    # Generate independent seeds for each trial
    trial_seeds = rng.integers(0, 2**31-1, size=n_trials)

    metrics_list = []

    for i, trial_seed in enumerate(trial_seeds):
        # Set seed for this trial
        np.random.seed(trial_seed)

        # Create fresh controller
        controller = controller_factory()

        # Run simulation
        from src.core.simulation_runner import run_simulation
        result = run_simulation(
            controller=controller,
            duration=cfg.simulation.duration,
            dt=cfg.simulation.dt,
            initial_state=cfg.simulation.initial_state
        )

        # Compute metrics
        from src.benchmarks.metrics import compute_all_metrics
        metrics = compute_all_metrics(
            result['time'],
            np.array(result['states']),
            np.array(result['controls']),
            max_force=cfg.controllers.max_force
        )

        metrics_list.append(metrics)

        # Progress callback
        if progress_callback:
            progress_callback(i + 1, n_trials)

    return metrics_list