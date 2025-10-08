# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 8
# Runnable: False
# Hash: 68d51eeb

# src/benchmarks/statistical_benchmarks_v2.py

def run_trials(controller_factory: Callable,
              cfg: Any,
              n_trials: int = 30,
              seed: Optional[int] = None,
              randomise_physics: bool = False,
              noise_std: float = 0.0) -> Tuple[List[dict], dict]:
    """Run statistical benchmark trials with confidence interval computation.

    Backward-compatible interface with enhanced capabilities.

    Parameters
    ----------
    controller_factory : callable
        Function returning fresh controller instance
    cfg : object
        Configuration object
    n_trials : int
        Number of trials (≥30 for CLT)
    seed : int, optional
        Random seed for reproducibility
    randomise_physics : bool
        Add physics parameter uncertainty
    noise_std : float
        Sensor noise standard deviation

    Returns
    -------
    metrics_list : list of dict
        Raw metrics from all trials
    ci_results : dict
        Confidence interval results for each metric

    Examples
    --------
    >>> metrics_list, ci_results = run_trials(
    ...     controller_factory=lambda: ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100),
    ...     cfg=config,
    ...     n_trials=30,
    ...     seed=42
    ... )
    >>> for metric, stats in ci_results.items():
    ...     print(f"{metric}: {stats['mean']:.4f} ± {stats['ci_width']:.4f}")
    """
    from .core import run_multiple_trials
    from .statistics import compute_t_confidence_intervals

    # Execute trials
    metrics_list = run_multiple_trials(
        controller_factory,
        cfg,
        n_trials=n_trials,
        seed=seed
    )

    # Compute confidence intervals
    ci_results = compute_t_confidence_intervals(metrics_list)

    return metrics_list, ci_results


def run_trials_with_advanced_statistics(controller_factory: Callable,
                                        cfg: Any,
                                        n_trials: int = 30,
                                        confidence_level: float = 0.95,
                                        use_bootstrap: bool = False,
                                        **kwargs) -> Tuple[List[dict], dict]:
    """Run trials with advanced statistical analysis.

    Enhanced version with non-parametric options.

    Parameters
    ----------
    use_bootstrap : bool
        Use bootstrap CI instead of t-distribution

    Returns
    -------
    metrics_list : list of dict
    analysis : dict
        Extended analysis including distribution tests
    """
    from .core import run_multiple_trials
    from .statistics import (
        compute_t_confidence_intervals,
        compute_bootstrap_confidence_intervals
    )

    metrics_list = run_multiple_trials(controller_factory, cfg, n_trials, **kwargs)

    if use_bootstrap:
        ci_results = compute_bootstrap_confidence_intervals(metrics_list, confidence_level)
    else:
        ci_results = compute_t_confidence_intervals(metrics_list, confidence_level)

    return metrics_list, ci_results


def compare_controllers(controller_a_factory: Callable,
                       controller_b_factory: Callable,
                       cfg: Any,
                       n_trials: int = 30,
                       metric: str = 'ise') -> dict:
    """Compare two controllers statistically.

    Parameters
    ----------
    controller_a_factory : callable
    controller_b_factory : callable
    cfg : object
    n_trials : int
    metric : str
        Metric for comparison

    Returns
    -------
    dict
        Comparison results with statistical significance
    """
    from .core import run_multiple_trials
    from .statistics import compare_controllers as compare_fn

    metrics_a = run_multiple_trials(controller_a_factory, cfg, n_trials)
    metrics_b = run_multiple_trials(controller_b_factory, cfg, n_trials)

    return compare_fn(metrics_a, metrics_b, metric)