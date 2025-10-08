# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 7
# Runnable: False
# Hash: 2af560cf

# src/benchmarks/statistics/confidence_intervals.py

def compute_t_confidence_intervals(metrics_list: List[dict],
                                  confidence_level: float = 0.95) -> dict:
    """Compute t-distribution confidence intervals for all metrics.

    Uses Student's t-distribution for small sample sizes (n < 100).

    Parameters
    ----------
    metrics_list : list of dict
        Metrics from multiple trials
    confidence_level : float
        Confidence level (default: 0.95 for 95% CI)

    Returns
    -------
    dict
        For each metric: {'mean': float, 'ci_width': float, 'ci_lower': float, 'ci_upper': float}

    Examples
    --------
    >>> ci_results = compute_t_confidence_intervals(metrics_list)
    >>> ise_mean = ci_results['ise']['mean']
    >>> ise_ci = ci_results['ise']['ci_width']
    >>> print(f"ISE: {ise_mean:.4f} ± {ise_ci:.4f}")
    """
    from scipy import stats

    # Extract metric names
    metric_names = list(metrics_list[0].keys())

    ci_results = {}

    for metric in metric_names:
        values = np.array([m[metric] for m in metrics_list])

        n = len(values)
        mean = np.mean(values)
        std = np.std(values, ddof=1)  # Bessel's correction
        sem = std / np.sqrt(n)  # Standard error of mean

        # t-critical value
        alpha = 1 - confidence_level
        t_crit = stats.t.ppf(1 - alpha/2, df=n-1)

        ci_width = t_crit * sem
        ci_lower = mean - ci_width
        ci_upper = mean + ci_width

        ci_results[metric] = {
            'mean': float(mean),
            'std': float(std),
            'ci_width': float(ci_width),
            'ci_lower': float(ci_lower),
            'ci_upper': float(ci_upper),
            'n': n
        }

    return ci_results


def compute_bootstrap_confidence_intervals(metrics_list: List[dict],
                                          confidence_level: float = 0.95,
                                          n_bootstrap: int = 10000) -> dict:
    """Compute bootstrap confidence intervals (non-parametric).

    Useful when metric distributions are non-normal.

    Parameters
    ----------
    metrics_list : list of dict
        Metrics from multiple trials
    confidence_level : float
        Confidence level
    n_bootstrap : int
        Number of bootstrap samples

    Returns
    -------
    dict
        Bootstrap CI results for each metric
    """
    metric_names = list(metrics_list[0].keys())
    ci_results = {}

    for metric in metric_names:
        values = np.array([m[metric] for m in metrics_list])

        # Bootstrap resampling
        bootstrap_means = []
        for _ in range(n_bootstrap):
            resample = np.random.choice(values, size=len(values), replace=True)
            bootstrap_means.append(np.mean(resample))

        bootstrap_means = np.array(bootstrap_means)

        # Percentile method
        alpha = 1 - confidence_level
        ci_lower = np.percentile(bootstrap_means, 100 * alpha/2)
        ci_upper = np.percentile(bootstrap_means, 100 * (1 - alpha/2))
        mean = np.mean(values)
        ci_width = (ci_upper - ci_lower) / 2

        ci_results[metric] = {
            'mean': float(mean),
            'ci_width': float(ci_width),
            'ci_lower': float(ci_lower),
            'ci_upper': float(ci_upper),
            'method': 'bootstrap'
        }

    return ci_results


def compare_controllers(metrics_a: List[dict], metrics_b: List[dict],
                       metric_name: str = 'ise',
                       alpha: float = 0.05) -> dict:
    """Compare two controllers using Welch's t-test.

    Welch's t-test handles unequal variances between groups.

    Parameters
    ----------
    metrics_a : list of dict
        Metrics from controller A
    metrics_b : list of dict
        Metrics from controller B
    metric_name : str
        Metric to compare (e.g., 'ise')
    alpha : float
        Significance level (default: 0.05)

    Returns
    -------
    dict
        Test results: {
            't_statistic': float,
            'p_value': float,
            'significant': bool,
            'mean_a': float,
            'mean_b': float,
            'better_controller': str
        }

    Examples
    --------
    >>> comparison = compare_controllers(classical_metrics, adaptive_metrics, 'ise')
    >>> if comparison['significant']:
    ...     print(f"{comparison['better_controller']} is significantly better (p={comparison['p_value']:.4f})")
    """
    from scipy import stats

    values_a = np.array([m[metric_name] for m in metrics_a])
    values_b = np.array([m[metric_name] for m in metrics_b])

    # Welch's t-test (unequal variances)
    t_stat, p_value = stats.ttest_ind(values_a, values_b, equal_var=False)

    mean_a = np.mean(values_a)
    mean_b = np.mean(values_b)

    significant = p_value < alpha
    better_controller = 'A' if mean_a < mean_b else 'B'

    return {
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'significant': bool(significant),
        'mean_a': float(mean_a),
        'mean_b': float(mean_b),
        'better_controller': better_controller,
        'effect_size': float(abs(mean_a - mean_b) / np.sqrt((np.var(values_a) + np.var(values_b)) / 2))
    }