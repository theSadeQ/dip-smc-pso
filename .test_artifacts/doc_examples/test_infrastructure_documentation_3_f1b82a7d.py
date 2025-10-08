# Example from: docs\test_infrastructure_documentation.md
# Index: 3
# Runnable: True
# Hash: f1b82a7d

@pytest.mark.slow
@pytest.mark.convergence
def test_pso_convergence_monte_carlo():
    """Monte Carlo analysis of PSO convergence properties."""
    # Runs 100+ optimization trials for statistical significance
    results = run_monte_carlo_pso_analysis(n_trials=100, n_iterations=200)
    assert results.convergence_rate > 0.95