# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 3
# Runnable: True
# Hash: edc43569

# src/benchmarks/metrics/stability_metrics.py

def compute_overshoot(x: np.ndarray, state_indices: List[int] = [1, 2]) -> float:
    """Compute maximum overshoot for angular states.

    Overshoot = max_{t∈[0,T]} |θᵢ(t)| for i ∈ {1,2}

    Safety-critical for physical systems.

    Parameters
    ----------
    x : np.ndarray
        State trajectories, shape (B, N, S) or (N, S)
    state_indices : list of int
        Indices of angular states (default: [1, 2] for θ1, θ2)

    Returns
    -------
    float
        Maximum overshoot [radians]
    """
    if x.ndim == 3:
        angular_states = x[:, :, state_indices]  # (B, N, 2)
        max_per_state = np.max(np.abs(angular_states), axis=1)  # (B, 2)
        max_overshoot = np.max(max_per_state, axis=1)  # (B,)
        return np.mean(max_overshoot)
    else:
        angular_states = x[:, state_indices]
        return np.max(np.abs(angular_states))


def compute_settling_time(t: np.ndarray, x: np.ndarray,
                          tolerance: float = 0.02) -> float:
    """Compute settling time to within tolerance of equilibrium.

    Settling time: minimum t where ||x(τ)|| < tolerance ∀ τ > t

    Parameters
    ----------
    t : np.ndarray
        Time vector
    x : np.ndarray
        State trajectories
    tolerance : float
        Settling tolerance (default: 0.02 = 2% of initial error)

    Returns
    -------
    float
        Settling time [seconds], or np.inf if never settles
    """
    if x.ndim == 3:
        errors = np.linalg.norm(x, axis=2)  # (B, N)
        settling_times = []

        for batch_errors in errors:
            settled_mask = batch_errors < tolerance
            if np.any(settled_mask):
                # Find first index where it stays below tolerance
                for i in range(len(settled_mask)):
                    if np.all(settled_mask[i:]):
                        settling_times.append(t[i])
                        break
                else:
                    settling_times.append(np.inf)
            else:
                settling_times.append(np.inf)

        return np.mean(settling_times)
    else:
        errors = np.linalg.norm(x, axis=1)
        settled_mask = errors < tolerance

        if np.any(settled_mask):
            for i in range(len(settled_mask)):
                if np.all(settled_mask[i:]):
                    return t[i]
        return np.inf


def compute_damping_ratio(x: np.ndarray, t: np.ndarray) -> float:
    """Estimate damping ratio from oscillatory response.

    Uses logarithmic decrement method:
        ζ = ln(x_peak1 / x_peak2) / √(4π² + ln²(x_peak1 / x_peak2))

    Parameters
    ----------
    x : np.ndarray
        State response (typically angular states)
    t : np.ndarray
        Time vector

    Returns
    -------
    float
        Estimated damping ratio (0 = undamped, 1 = critically damped)
    """
    from scipy.signal import find_peaks

    # Find peaks in response
    peaks, _ = find_peaks(np.abs(x))

    if len(peaks) < 2:
        return 1.0  # No oscillation = critically damped or overdamped

    # Use first two peaks for logarithmic decrement
    x1 = np.abs(x[peaks[0]])
    x2 = np.abs(x[peaks[1]])

    if x2 == 0:
        return 1.0

    delta = np.log(x1 / x2)  # Logarithmic decrement
    zeta = delta / np.sqrt(4 * np.pi**2 + delta**2)

    return min(zeta, 1.0)  # Cap at 1.0