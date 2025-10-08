# Example from: docs\guides\api\optimization.md
# Index: 7
# Runnable: True
# Hash: 2de42b24

def energy_efficient_cost(gains):
    """Optimize for energy efficiency."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = runner.run(controller)

    # Total control energy
    control_effort = result['metrics']['control_effort']
    return control_effort