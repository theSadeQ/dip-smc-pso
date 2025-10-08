# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 14
# Runnable: False
# Hash: d1189f0b

def create_smc_for_pso(smc_type: SMCType,
                      gains: List[float],
                      max_force: float = 100.0,
                      dt: float = 0.01) -> PSOControllerWrapper:
    """
    Create SMC controller optimized for PSO fitness functions.

    This is the primary function for PSO integration, providing:
    - Single-line controller creation
    - Automatic gain validation
    - Simplified control interface
    - Error handling for invalid parameters

    Args:
        smc_type: Controller type from SMCType enum
        gains: Gain array from PSO optimization
        max_force: Control force saturation limit
        dt: Control timestep

    Returns:
        PSOControllerWrapper with simplified interface

    Example:
        # In PSO fitness function
        def evaluate_gains(gains_array):
            controller = create_smc_for_pso(SMCType.CLASSICAL, gains_array)
            result = run_simulation(controller)
            return compute_fitness(result)
    """