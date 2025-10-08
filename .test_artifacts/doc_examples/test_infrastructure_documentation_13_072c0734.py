# Example from: docs\test_infrastructure_documentation.md
# Index: 13
# Runnable: False
# Hash: 072c0734

# example-metadata:
# runnable: false

@pytest.mark.end_to_end
@pytest.mark.slow
def test_complete_optimization_workflow():
    """Test complete workflow: config → optimization → validation → deployment."""

    # 1. Load configuration
    config = load_config("config.yaml")

    # 2. Run PSO optimization
    optimizer = create_optimizer_from_config(config)
    optimization_result = optimizer.optimize("hybrid_adaptive_sta_smc")

    # 3. Validate optimized controller
    controller = create_controller("hybrid_adaptive_sta_smc", gains=optimization_result.best_gains)
    validation_score = validate_controller_performance(controller)

    # 4. Check deployment readiness
    assert validation_score.stability_margin > 0.5
    assert validation_score.performance_index < 5.0
    assert validation_score.robustness_score > 0.8