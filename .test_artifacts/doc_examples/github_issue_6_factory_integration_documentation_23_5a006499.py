# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 23
# Runnable: True
# Hash: 5a006499

# Gradually adopt new factory for new code
from controllers import create_smc_for_pso, SMCType
from controllers.factory import create_controller_legacy

# New PSO-optimized code
def new_optimization_workflow():
    controller = create_smc_for_pso(
        SMCType.CLASSICAL,
        [10, 8, 15, 12, 50, 5]
    )
    return run_pso_optimization(controller)

# Existing legacy code unchanged
def existing_simulation_workflow():
    controller = create_controller_legacy(
        "classical_smc",
        gains=[10, 8, 15, 12, 50, 5]
    )
    return run_simulation(controller)