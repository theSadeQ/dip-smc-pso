# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 18
# Runnable: True
# Hash: 4f7c528e

# tests/test_integration/test_pso_hybrid_integration.py
def test_pso_hybrid_integration_no_errors(caplog):
    """Test PSO optimization with hybrid controller produces no errors."""

    # Run PSO optimization
    from src.optimizer.pso_optimizer import PSOTuner

    tuner = PSOTuner(
        bounds=[(1, 100), (1, 100), (1, 20), (1, 20)],
        n_particles=5,  # Small for testing
        iters=10
    )

    best_gains, best_cost = tuner.optimize(
        controller_type='hybrid_adaptive_sta_smc',
        dynamics=test_dynamics
    )

    # Verify no errors in logs
    error_logs = [record for record in caplog.records if record.levelname == 'ERROR']
    assert len(error_logs) == 0, f"Found error logs: {[r.message for r in error_logs]}"

    # Verify successful optimization
    assert isinstance(best_gains, list)
    assert len(best_gains) == 4
    assert isinstance(best_cost, float)
    assert best_cost >= 0.0