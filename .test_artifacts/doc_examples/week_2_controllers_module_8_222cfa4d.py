# Example from: docs\plans\documentation\week_2_controllers_module.md
# Index: 8
# Runnable: True
# Hash: 222cfa4d

def fitness_function(gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    performance = evaluate(controller)
    return performance