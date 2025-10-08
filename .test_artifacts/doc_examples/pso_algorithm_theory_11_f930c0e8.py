# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 11
# Runnable: False
# Hash: f930c0e8

def evaluate_fitness(gains):
    """Evaluate controller performance via simulation."""
    # 1. Create controller
    controller = create_controller('classical_smc', gains=gains)

    # 2. Run simulation (5-second horizon)
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

    return fitness