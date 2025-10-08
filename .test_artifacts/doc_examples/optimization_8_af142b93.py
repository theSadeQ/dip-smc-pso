# Example from: docs\guides\api\optimization.md
# Index: 8
# Runnable: False
# Hash: af142b93

def multi_objective_cost(gains, w_ise=0.6, w_energy=0.3, w_time=0.1):
    """Balance tracking, energy, and speed."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = runner.run(controller)

    # Normalize metrics
    ise_normalized = result['metrics']['ise'] / 10.0
    energy_normalized = result['metrics']['control_effort'] / 5000.0
    time_normalized = result['metrics']['settling_time'] / 5.0

    # Weighted sum
    total_cost = (w_ise * ise_normalized +
                  w_energy * energy_normalized +
                  w_time * time_normalized)

    return total_cost

# Use with tuner
tuner = PSOTuner(
    controller_type=SMCType.CLASSICAL,
    bounds=bounds,
    cost_function=multi_objective_cost
)