# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 12
# Runnable: False
# Hash: 60afbf2d

def test_pso_integration_no_errors(controller_name, caplog):
    """Test PSO optimization produces no runtime errors."""
    tuner = PSOTuner(bounds=get_bounds(controller_name), n_particles=5, iters=10)

    best_gains, best_cost = tuner.optimize(
        controller_type=controller_name,
        dynamics=test_dynamics
    )

    # Verify no error logs
    error_logs = [r for r in caplog.records if r.levelname == 'ERROR']
    assert len(error_logs) == 0, f"Found errors: {[r.message for r in error_logs]}"

    # Verify valid optimization results
    assert isinstance(best_cost, float)
    assert best_cost >= 0.0