# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 2
# Runnable: False
# Hash: 69214df7

# example-metadata:
# runnable: false

# src/benchmarks/metrics/control_metrics.py

def compute_ise(t: np.ndarray, x: np.ndarray) -> float:
    """Compute Integral of Squared Error (ISE).

    ISE = ∫₀ᵀ ||x(t)||² dt

    Physical Interpretation:
        Measures cumulative deviation from desired trajectory.
        Lower values indicate better tracking performance.

    Control Engineering Context:
        - Quadratic cost function component in optimal control
        - Related to H₂ norm of closed-loop system
        - Emphasizes large deviations more than small ones

    Parameters
    ----------
    t : np.ndarray
        Time vector, shape (N+1,)
    x : np.ndarray
        State trajectories, shape (B, N+1, S) for B batches, S states

    Returns
    -------
    float
        ISE value averaged across batch dimension

    Examples
    --------
    >>> t = np.linspace(0, 5, 501)
    >>> x = np.random.randn(10, 501, 6)  # 10 trials, 6 states
    >>> ise = compute_ise(t, x)
    >>> print(f"ISE: {ise:.4f}")
    """
    dt = t[1] - t[0]

    # Handle batched or single trajectory
    if x.ndim == 3:  # Batched: (B, N, S)
        squared_errors = np.sum(x**2, axis=2)  # Sum over states
        ise_per_batch = np.sum(squared_errors, axis=1) * dt
        return np.mean(ise_per_batch)
    else:  # Single trajectory: (N, S)
        squared_errors = np.sum(x**2, axis=1)
        return np.sum(squared_errors) * dt


def compute_itae(t: np.ndarray, x: np.ndarray) -> float:
    """Compute Integral of Time-weighted Absolute Error (ITAE).

    ITAE = ∫₀ᵀ t·||x(t)|| dt

    Emphasizes errors occurring later in the trajectory.
    Penalizes sustained deviations more heavily than transient errors.

    Parameters
    ----------
    t : np.ndarray
        Time vector
    x : np.ndarray
        State trajectories

    Returns
    -------
    float
        ITAE value

    Notes
    -----
    ITAE is preferred for evaluating settling characteristics because:
    - Late-stage errors receive higher penalty
    - Encourages faster settling to equilibrium
    - Better reflects control quality in stabilization tasks
    """
    dt = t[1] - t[0]

    if x.ndim == 3:
        abs_errors = np.linalg.norm(x, axis=2)  # (B, N)
        time_weighted = abs_errors * t[np.newaxis, :]
        itae_per_batch = np.sum(time_weighted, axis=1) * dt
        return np.mean(itae_per_batch)
    else:
        abs_errors = np.linalg.norm(x, axis=1)
        time_weighted = abs_errors * t
        return np.sum(time_weighted) * dt


def compute_rms_control(t: np.ndarray, u: np.ndarray) -> float:
    """Compute RMS (Root Mean Square) control effort.

    RMS_u = √(1/T ∫₀ᵀ u(t)² dt)

    Measures average control energy consumption.
    Important for actuator sizing and power requirements.

    Parameters
    ----------
    t : np.ndarray
        Time vector
    u : np.ndarray
        Control history

    Returns
    -------
    float
        RMS control effort [Force]
    """
    dt = t[1] - t[0]
    T = t[-1] - t[0]

    if u.ndim == 2:  # Batched
        squared_control = u**2
        integral = np.sum(squared_control, axis=1) * dt
        rms_per_batch = np.sqrt(integral / T)
        return np.mean(rms_per_batch)
    else:
        squared_control = u**2
        integral = np.sum(squared_control) * dt
        return np.sqrt(integral / T)


def compute_control_rate(t: np.ndarray, u: np.ndarray) -> float:
    """Compute RMS control rate (slew rate).

    du_RMS = √(1/T ∫₀ᵀ (du/dt)² dt)

    Measures control signal smoothness.
    High values indicate chattering or aggressive switching.

    Parameters
    ----------
    t : np.ndarray
        Time vector
    u : np.ndarray
        Control history

    Returns
    -------
    float
        RMS control rate [Force/time]

    Notes
    -----
    Critical for:
    - Actuator wear and lifetime estimation
    - Implementation feasibility (discrete-time constraints)
    - Chattering quantification in sliding mode control
    """
    dt = t[1] - t[0]

    if u.ndim == 2:
        du_dt = np.diff(u, axis=1) / dt
        return compute_rms_control(t[:-1], du_dt)
    else:
        du_dt = np.diff(u) / dt
        return compute_rms_control(t[:-1], du_dt)