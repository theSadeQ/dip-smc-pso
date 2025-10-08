# Example from: docs\deployment_validation_checklists.md
# Index: 4
# Runnable: False
# Hash: 531edca1

# example-metadata:
# runnable: false

def test_pso_integration():
    """Test PSO optimization integration."""
    optimizer = PSOOptimizer()
    controller_factory = ControllerFactory()

    # Test optimization workflow
    best_params = optimizer.optimize(
        controller_type='classical_smc',
        factory=controller_factory,
        bounds=optimization_bounds
    )

    # Validate optimized parameters
    assert all(bounds[0] <= param <= bounds[1] for param, bounds in zip(best_params, optimization_bounds))

    # Test optimized controller performance
    controller = controller_factory.create_controller('classical_smc', gains=best_params)
    performance = evaluate_controller_performance(controller)
    assert performance.stability_achieved
    assert performance.settling_time < max_settling_time

    return True