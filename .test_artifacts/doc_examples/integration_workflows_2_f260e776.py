# Example from: docs\testing\guides\integration_workflows.md
# Index: 2
# Runnable: False
# Hash: f260e776

def test_pso_tuning_workflow():
    """Test complete PSO tuning pipeline"""
    # Define optimization problem
    bounds = [(1, 100), (1, 100), (1, 100), (1, 100), (1, 100), (0.1, 10)]

    def fitness(gains):
        controller = ClassicalSMC(gains=gains)
        cost = evaluate_controller(controller, test_scenarios)
        return cost

    # Run PSO
    tuner = PSOTuner(n_particles=30, iterations=50, bounds=bounds)
    result = tuner.optimize(fitness)

    # Validate result
    assert result['cost'] < 1.0, "PSO did not find good solution"
    assert len(result['best_gains']) == 6, "Incorrect number of gains"

    # Test optimized controller
    optimized_controller = ClassicalSMC(gains=result['best_gains'])
    performance = evaluate_controller(optimized_controller, validation_scenarios)
    assert performance < 0.5, "Optimized controller underperforms"