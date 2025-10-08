# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 4
# Runnable: False
# Hash: d56fe1fc

# example-metadata:
# runnable: false

# src/benchmarks/metrics/constraint_metrics.py

def count_control_violations(u: np.ndarray, max_force: float) -> int:
    """Count control saturation violations.

    Violations = |{t : |u(t)| > u_max}|

    Zero violations required for safe operation.

    Parameters
    ----------
    u : np.ndarray
        Control history
    max_force : float
        Maximum allowable control force

    Returns
    -------
    int
        Number of timesteps exceeding limit
    """
    if u.ndim == 2:
        violations_per_batch = np.sum(np.abs(u) > max_force, axis=1)
        return int(np.mean(violations_per_batch))
    else:
        return int(np.sum(np.abs(u) > max_force))


def compute_violation_severity(u: np.ndarray, max_force: float) -> float:
    """Compute severity of constraint violations.

    Severity = (1/N) Σ max(0, |u(t)| - u_max)

    Quantifies how far violations exceed limits.

    Parameters
    ----------
    u : np.ndarray
        Control history
    max_force : float
        Maximum allowable control force

    Returns
    -------
    float
        Average violation severity [Force]
    """
    if u.ndim == 2:
        excess = np.maximum(0, np.abs(u) - max_force)
        return np.mean(np.mean(excess, axis=1))
    else:
        excess = np.maximum(0, np.abs(u) - max_force)
        return np.mean(excess)