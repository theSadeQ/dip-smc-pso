# Example from: docs\configuration_schema_validation.md
# Index: 9
# Runnable: False
# Hash: 5b254053

def validate_pso_convergence_constraints(pso_config: dict) -> bool:
    """Validate PSO convergence mathematical constraints."""

    w = pso_config['w']
    c1 = pso_config['c1']
    c2 = pso_config['c2']

    # Constriction factor stability
    phi = c1 + c2
    if phi <= 4.0:
        raise ValueError("PSO stability requires c₁ + c₂ > 4")

    # Calculate constriction factor
    chi = 2 / (2 - phi - np.sqrt(phi**2 - 4*phi))
    if chi >= 1.0:
        raise ValueError("Constriction factor ≥ 1, system unstable")

    # Velocity convergence
    if w * chi >= 1.0:
        raise ValueError("Velocity update factor exceeds stability limit")

    # Swarm diversity constraints
    n_particles = pso_config['n_particles']
    if n_particles < 10:
        raise ValueError("Insufficient particles for swarm diversity")

    # Search space constraints
    for controller_bounds in pso_config['bounds'].values():
        for bound_pair in controller_bounds:
            min_val, max_val = bound_pair
            search_ratio = max_val / min_val
            if search_ratio > 1000:
                raise ValueError("Search space too large for PSO convergence")

    return True