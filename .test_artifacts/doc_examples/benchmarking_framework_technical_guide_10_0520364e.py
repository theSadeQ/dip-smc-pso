# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 10
# Runnable: False
# Hash: 0520364e

# example-metadata:
# runnable: false

# benchmarks/analysis/accuracy_metrics.py

def compute_energy_conservation(t: np.ndarray, x: np.ndarray,
                               physics_params: dict) -> dict:
    """Analyze energy conservation for Hamiltonian systems.

    Parameters
    ----------
    t : np.ndarray
        Time vector
    x : np.ndarray
        State trajectories
    physics_params : dict
        Physics parameters

    Returns
    -------
    dict
        {
            'initial_energy': float,
            'final_energy': float,
            'max_drift': float,
            'relative_drift': float
        }
    """
    def compute_energy(state):
        # Kinetic energy
        x_dot, theta1_dot, theta2_dot = state[3], state[4], state[5]
        KE = 0.5 * physics_params['M'] * x_dot**2  # Cart
        # ... (pendulum kinetic energy)

        # Potential energy
        theta1, theta2 = state[1], state[2]
        PE = physics_params['m1'] * physics_params['g'] * physics_params['L1'] * (1 - np.cos(theta1))
        # ... (second pendulum PE)

        return KE + PE

    energies = np.array([compute_energy(state) for state in x])

    initial_energy = energies[0]
    final_energy = energies[-1]
    max_drift = np.max(np.abs(energies - initial_energy))
    relative_drift = max_drift / initial_energy if initial_energy != 0 else np.inf

    return {
        'initial_energy': float(initial_energy),
        'final_energy': float(final_energy),
        'max_drift': float(max_drift),
        'relative_drift': float(relative_drift),
        'energies': energies
    }


def estimate_convergence_order(integrator, x0: np.ndarray, t_span: tuple,
                              dt_values: List[float]) -> dict:
    """Estimate numerical convergence order.

    Uses Richardson extrapolation to estimate p in:
        e_h = C·h^p

    Parameters
    ----------
    integrator : object
        Integration method instance
    x0 : np.ndarray
        Initial state
    t_span : tuple
        Time span
    dt_values : list of float
        Decreasing time steps for convergence analysis

    Returns
    -------
    dict
        {
            'convergence_order': float,
            'errors': list of float,
            'dt_values': list of float
        }
    """
    # Get reference solution (finest dt)
    ref_dt = min(dt_values) / 4
    ref_result = integrator.integrate(x0, t_span, ref_dt)
    ref_x_final = ref_result['x'][-1]

    errors = []
    for dt in dt_values:
        result = integrator.integrate(x0, t_span, dt)
        x_final = result['x'][-1]
        error = np.linalg.norm(x_final - ref_x_final)
        errors.append(error)

    # Estimate convergence order: p = log(e_h1/e_h2) / log(h1/h2)
    orders = []
    for i in range(len(errors) - 1):
        if errors[i+1] > 0:
            order = np.log(errors[i] / errors[i+1]) / np.log(dt_values[i] / dt_values[i+1])
            orders.append(order)

    avg_order = np.mean(orders) if orders else np.nan

    return {
        'convergence_order': float(avg_order),
        'errors': [float(e) for e in errors],
        'dt_values': dt_values
    }