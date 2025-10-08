# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 15
# Runnable: False
# Hash: bc837548

def get_gain_bounds_for_pso(smc_type: SMCType) -> List[Tuple[float, float]]:
    """
    Get mathematically-derived PSO bounds for controller type.

    Bounds are based on:
    - Lyapunov stability requirements
    - Performance specifications
    - Physical system limitations
    - Practical implementation constraints

    Args:
        smc_type: Controller type from SMCType enum

    Returns:
        List of (lower_bound, upper_bound) for each gain

    Example:
        bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
        # Returns: [(0.1, 50.0), (0.1, 50.0), (1.0, 50.0),
        #           (1.0, 50.0), (1.0, 200.0), (0.0, 50.0)]
    """