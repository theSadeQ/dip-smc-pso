# Example from: docs\guides\api\optimization.md
# Index: 6
# Runnable: True
# Hash: f32090c1

def settling_time_cost(gains):
    """Optimize for fast settling."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = runner.run(controller)

    # Penalize slow settling
    settling_time = result['metrics']['settling_time']
    if settling_time > 3.0:
        return 1000.0 + settling_time  # Large penalty

    return settling_time