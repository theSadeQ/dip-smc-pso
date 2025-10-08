# Example from: docs\test_infrastructure_validation_report.md
# Index: 3
# Runnable: True
# Hash: 40d9d3c5

@pytest.mark.statistical
@pytest.mark.convergence
def test_pso_convergence_monte_carlo():
    """Statistical validation of PSO convergence properties."""
    # Multiple independent runs for confidence intervals
    # Convergence rate analysis: P(convergence) > 0.95
    # Performance distribution characterization