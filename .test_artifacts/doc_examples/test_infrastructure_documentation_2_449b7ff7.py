# Example from: docs\test_infrastructure_documentation.md
# Index: 2
# Runnable: True
# Hash: 449b7ff7

@pytest.mark.integration
def test_pso_controller_optimization():
    """Test PSO optimization of controller parameters."""
    optimizer = PSOTuner(bounds=[(0.1, 50.0)] * 6)
    controller_type = "classical_smc"
    result = optimizer.optimize(controller_type, n_particles=20, n_iterations=50)
    assert result.success
    assert len(result.best_gains) == 6