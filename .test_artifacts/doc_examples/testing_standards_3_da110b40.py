# Example from: docs\testing\standards\testing_standards.md
# Index: 3
# Runnable: False
# Hash: da110b40

# example-metadata:
# runnable: false

def test_complete_pso_optimization_workflow():
    """Test complete PSO optimization workflow from CLI to results."""
    # Setup configuration
    config = create_test_config(
        controller_type="classical_smc",
        pso_iterations=10,  # Reduced for testing
        pso_particles=5
    )

    # Execute workflow
    results = run_pso_optimization_workflow(config)

    # Verify results
    assert results.optimization_successful
    assert len(results.optimized_gains) == 6
    assert results.final_cost < results.initial_cost
    assert all(0.1 <= gain <= 100.0 for gain in results.optimized_gains)

    # Verify simulation with optimized gains
    controller = create_controller_from_gains(results.optimized_gains)
    simulation_result = run_simulation(controller, config.simulation)
    assert simulation_result.successful
    assert simulation_result.final_state_error < 0.1