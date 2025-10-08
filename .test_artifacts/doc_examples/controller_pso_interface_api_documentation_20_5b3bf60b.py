# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 20
# Runnable: True
# Hash: 5b3bf60b

def test_pso_optimization_integration(controller_type: str):
    """Test complete PSO optimization workflow."""
    from src.config import load_config
    from src.optimization.algorithms.pso_optimizer import PSOTuner

    # Load test configuration
    config = load_config('config.yaml')

    # Create controller factory
    def factory(gains: np.ndarray):
        return ControllerFactory.create_controller(controller_type, gains)

    # Initialize PSO tuner
    pso_tuner = PSOTuner(
        controller_factory=factory,
        config=config,
        seed=42  # Reproducible testing
    )

    # Run short optimization
    bounds_config = getattr(config.pso.bounds, controller_type)
    lower_bounds = np.array(bounds_config.lower)
    upper_bounds = np.array(bounds_config.upper)

    results = pso_tuner.optimize(
        bounds=(lower_bounds, upper_bounds),
        n_particles=10,  # Small for testing
        n_iterations=5   # Short for testing
    )

    # Validate results
    assert 'best_gains' in results, "Results missing best_gains"
    assert 'best_cost' in results, "Results missing best_cost"
    assert 'success' in results, "Results missing success flag"

    best_gains = results['best_gains']
    assert len(best_gains) == len(lower_bounds), "Invalid best_gains dimension"
    assert np.all(best_gains >= lower_bounds), "best_gains violate lower bounds"
    assert np.all(best_gains <= upper_bounds), "best_gains violate upper bounds"

    # Test optimized controller creation
    optimized_controller = factory(best_gains)
    test_state = np.zeros(6)
    control = optimized_controller.compute_control(test_state)
    assert np.isfinite(control), "Optimized controller produces invalid control"