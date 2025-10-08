# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 5
# Runnable: True
# Hash: 4d09dc2c

# src/benchmarks/metrics/__init__.py

from .control_metrics import compute_ise, compute_itae, compute_rms_control, compute_control_rate
from .stability_metrics import compute_overshoot, compute_settling_time, compute_damping_ratio
from .constraint_metrics import count_control_violations, compute_violation_severity

__all__ = [
    'compute_all_metrics',
    'compute_basic_metrics',
    'compute_ise',
    'compute_itae',
    'compute_rms_control',
    'compute_overshoot',
    'count_control_violations'
]


def compute_all_metrics(t: np.ndarray, x: np.ndarray, u: np.ndarray,
                       max_force: float, include_advanced: bool = False) -> dict:
    """Compute all performance metrics for a simulation result.

    Parameters
    ----------
    t : np.ndarray
        Time vector
    x : np.ndarray
        State trajectories
    u : np.ndarray
        Control history
    max_force : float
        Maximum control force limit
    include_advanced : bool
        Include advanced metrics (settling time, damping ratio)

    Returns
    -------
    dict
        Dictionary of all computed metrics

    Examples
    --------
    >>> metrics = compute_all_metrics(t, x, u, max_force=100.0)
    >>> print(f"ISE: {metrics['ise']:.4f}")
    >>> print(f"Violations: {metrics['violations']}")
    """
    metrics = {
        'ise': compute_ise(t, x),
        'itae': compute_itae(t, x),
        'rms_control': compute_rms_control(t, u),
        'control_rate': compute_control_rate(t, u),
        'overshoot': compute_overshoot(x),
        'violations': count_control_violations(u, max_force),
        'violation_severity': compute_violation_severity(u, max_force)
    }

    if include_advanced:
        metrics['settling_time'] = compute_settling_time(t, x)
        metrics['damping_ratio'] = compute_damping_ratio(x[:, 1], t)  # θ1 response

    return metrics


def compute_basic_metrics(t: np.ndarray, x: np.ndarray, u: np.ndarray) -> dict:
    """Compute basic performance metrics (no max_force required).

    Minimal metric set for quick analysis.
    """
    return {
        'ise': compute_ise(t, x),
        'rms_control': compute_rms_control(t, u),
        'overshoot': compute_overshoot(x)
    }