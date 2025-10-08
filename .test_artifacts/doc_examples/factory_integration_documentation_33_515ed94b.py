# Example from: docs\factory_integration_documentation.md
# Index: 33
# Runnable: False
# Hash: 515ed94b

# example-metadata:
# runnable: false

# Avoid creating unnecessary controllers
def optimize_controller_creation():
    # ❌ Creates many controller instances
    controllers = []
    for gains_set in gain_sets:
        controller = create_controller('classical_smc', gains=gains_set)
        controllers.append(controller)

    # ✅ Use single factory function
    factory = create_pso_controller_factory(SMCType.CLASSICAL)
    controllers = [factory(gains_set) for gains_set in gain_sets]