# Example from: docs\guides\api\optimization.md
# Index: 5
# Runnable: True
# Hash: aeca6cb1

def default_cost_function(gains):
    """Default: Minimize ISE for angle tracking."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = runner.run(controller)
    return result['metrics']['ise']