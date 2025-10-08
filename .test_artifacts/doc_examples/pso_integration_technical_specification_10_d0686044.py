# Example from: docs\pso_integration_technical_specification.md
# Index: 10
# Runnable: False
# Hash: d0686044

# example-metadata:
# runnable: false

class PSO_QualityGates:
    """
    Automated quality gates for PSO integration deployment.
    """

    @staticmethod
    def validate_optimization_result(result: Dict[str, Any],
                                   test_config: TestConfig) -> QualityGateResult:
        """
        Comprehensive quality gate validation for PSO optimization results.
        """
        checks = []

        # Performance Gate
        final_cost = result['best_cost']
        checks.append(QualityCheck(
            name="Performance",
            passed=final_cost < test_config.max_acceptable_cost,
            value=final_cost,
            threshold=test_config.max_acceptable_cost
        ))

        # Stability Gate
        optimized_gains = result['best_pos']
        stability_valid, stability_msg = validate_controller_stability(optimized_gains)
        checks.append(QualityCheck(
            name="Stability",
            passed=stability_valid,
            message=stability_msg
        ))

        # Convergence Gate
        cost_history = result['history']['cost']
        converged = check_convergence_quality(cost_history)
        checks.append(QualityCheck(
            name="Convergence",
            passed=converged,
            message=f"Converged in {len(cost_history)} iterations"
        ))

        # Issue #2 Regression Gate (STA-SMC specific)
        if test_config.controller_type == 'sta_smc':
            overshoot = simulate_and_measure_overshoot(optimized_gains)
            checks.append(QualityCheck(
                name="Issue2_Regression",
                passed=overshoot < 0.05,  # 5% threshold
                value=overshoot,
                threshold=0.05
            ))

        overall_passed = all(check.passed for check in checks)
        return QualityGateResult(passed=overall_passed, checks=checks)