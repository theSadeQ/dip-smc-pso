# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 8
# Runnable: False
# Hash: 0e3e8dab

# example-metadata:
# runnable: false

def objective_function_smc(gains: np.ndarray) -> float:
    """Fitness function for SMC gain tuning.

    Args:
        gains: Controller gains [k1, k2, λ1, λ2, K, kd]

    Returns:
        Fitness value (lower is better)
    """
    # 1. Create controller
    controller = create_controller('classical_smc', gains=gains)

    # 2. Run simulation
    result = simulate(
        controller=controller,
        duration=5.0,
        dt=0.01,
        initial_state=[0.1, 0.05, 0, 0, 0, 0]
    )

    # 3. Compute metrics
    ise = np.trapz(result.states**2, dx=0.01)
    chattering = np.sum(np.abs(np.diff(result.control))) * 0.01
    effort = np.trapz(result.control**2, dx=0.01)

    # 4. Multi-objective fitness
    fitness = 0.5 * ise + 0.3 * chattering + 0.2 * effort

    # 5. Constraint penalty
    if any(g <= 0 for g in gains[:5]):  # Stability constraint
        fitness += 1e6

    return fitness