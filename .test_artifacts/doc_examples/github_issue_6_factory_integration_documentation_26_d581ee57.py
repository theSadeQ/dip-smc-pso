# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 26
# Runnable: True
# Hash: d581ee57

def fitness_function(gains_array):
    # Automatic validation and simplified creation
    controller = create_smc_for_pso(
        SMCType.CLASSICAL,
        gains_array.tolist()
    )
    result = run_simulation(controller)
    return compute_fitness(result)
    # Note: Invalid gains automatically handled with appropriate penalties