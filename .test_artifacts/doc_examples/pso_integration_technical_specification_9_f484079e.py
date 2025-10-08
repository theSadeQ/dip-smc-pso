# Example from: docs\pso_integration_technical_specification.md
# Index: 9
# Runnable: False
# Hash: f484079e

# example-metadata:
# runnable: false

class PSO_IntegrationTestSuite:
    """
    Comprehensive integration testing for PSO-controller system.
    """

    def test_controller_factory_integration(self):
        """
        Test 1: Controller Factory PSO Compatibility

        Acceptance Criteria:
        ✓ Factory function has required n_gains attribute
        ✓ All controller types instantiate with PSO-provided gains
        ✓ Controller validation methods work correctly
        ✓ Memory usage remains bounded during batch creation
        """

    def test_pso_optimization_convergence(self):
        """
        Test 2: PSO Optimization Convergence

        Acceptance Criteria:
        ✓ Convergence within 200 iterations for standard test cases
        ✓ Final cost < 0.1 for nominal initial conditions
        ✓ Optimized gains satisfy stability constraints
        ✓ Reproducible results with fixed random seed
        """

    def test_uncertainty_robustness(self):
        """
        Test 3: Robust Optimization Under Uncertainty

        Acceptance Criteria:
        ✓ Monte Carlo evaluation completes without errors
        ✓ Robust gains show ≤10% performance degradation across uncertainty
        ✓ Confidence intervals properly computed and reasonable
        ✓ No numerical instabilities during uncertainty sampling
        """

    def test_bounds_validation_enforcement(self):
        """
        Test 4: Bounds Validation and Enforcement

        Acceptance Criteria:
        ✓ Out-of-bounds particles properly penalized
        ✓ Controller-specific stability constraints enforced
        ✓ STA-SMC K₁ > K₂ condition always satisfied
        ✓ Damping ratio bounds maintained for surface coefficients
        """

    def test_performance_regression(self):
        """
        Test 5: Performance Regression Detection

        Acceptance Criteria:
        ✓ Issue #2 overshoot resolution maintained (<5% overshoot)
        ✓ Optimization time ≤ 60 seconds for standard configuration
        ✓ Memory usage ≤ 2GB during full PSO run
        ✓ All controller types achieve acceptable performance
        """