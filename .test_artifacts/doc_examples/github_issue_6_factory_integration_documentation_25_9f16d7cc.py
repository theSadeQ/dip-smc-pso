# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 25
# Runnable: False
# Hash: 9f16d7cc

def fitness_function(gains_array):
    # Manual controller creation with error handling
    try:
        controller = create_controller(
            "classical_smc",
            gains=gains_array.tolist(),
            max_force=100.0,
            boundary_layer=0.01
        )
        result = run_simulation(controller)
        return compute_fitness(result)
    except Exception:
        return 1000.0  # Penalty for invalid gains