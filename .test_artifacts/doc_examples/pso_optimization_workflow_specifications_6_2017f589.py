# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 6
# Runnable: False
# Hash: 2017f589

class QualityGateSystem:
    """
    Automated quality gate system for PSO optimization workflow.
    """

    def __init__(self, config: dict):
        self.config = config
        self.quality_gates = [
            ConfigurationQualityGate(),
            OptimizationQualityGate(),
            PerformanceQualityGate(),
            SafetyQualityGate(),
            Issue2ComplianceQualityGate(),
            RegressionQualityGate()
        ]

    def evaluate_quality_gates(self, workflow_result: dict) -> QualityGateReport:
        """
        Evaluate all quality gates and generate comprehensive report.
        """
        report = QualityGateReport()

        for gate in self.quality_gates:
            gate_result = gate.evaluate(workflow_result, self.config)
            report.add_gate_result(gate.name, gate_result)

        # Generate overall assessment
        report.generate_overall_assessment()

        return report

class Issue2ComplianceQualityGate(QualityGate):
    """
    Quality gate specifically for Issue #2 overshoot compliance.
    """

    def __init__(self):
        self.name = "Issue2_Overshoot_Compliance"
        self.acceptance_criteria = {
            'max_predicted_overshoot': 5.0,    # % maximum theoretical overshoot
            'min_damping_ratio': 0.69,         # Minimum damping for compliance
            'max_lambda_bounds': 10.0,         # Maximum lambda values
            'simulation_overshoot_limit': 5.0   # % maximum measured overshoot
        }

    def evaluate(self, workflow_result: dict, config: dict) -> QualityGateResult:
        """
        Evaluate Issue #2 overshoot compliance.
        """
        result = QualityGateResult(gate_name=self.name)

        # Skip if not STA-SMC
        if config.get('controller_type') != 'sta_smc':
            result.status = 'SKIPPED'
            result.message = 'Issue #2 compliance only applies to STA-SMC'
            return result

        optimized_gains = workflow_result.get('best_gains')
        if optimized_gains is None or len(optimized_gains) < 6:
            result.status = 'FAILED'
            result.message = 'Missing or insufficient optimized gains'
            return result

        # Extract surface coefficients
        lambda1, lambda2 = optimized_gains[4], optimized_gains[5]
        k1, k2 = optimized_gains[2], optimized_gains[3]

        # Check 1: Lambda bounds compliance
        lambda_bounds_ok = (lambda1 <= self.acceptance_criteria['max_lambda_bounds'] and
                          lambda2 <= self.acceptance_criteria['max_lambda_bounds'])

        # Check 2: Damping ratio compliance
        zeta1 = lambda1 / (2 * np.sqrt(k1))
        zeta2 = lambda2 / (2 * np.sqrt(k2))
        damping_ok = (zeta1 >= self.acceptance_criteria['min_damping_ratio'] and
                     zeta2 >= self.acceptance_criteria['min_damping_ratio'])

        # Check 3: Predicted overshoot
        avg_zeta = (zeta1 + zeta2) / 2
        if avg_zeta < 1.0:
            predicted_overshoot = 100 * np.exp(-avg_zeta * np.pi / np.sqrt(1 - avg_zeta**2))
        else:
            predicted_overshoot = 0.0

        overshoot_prediction_ok = predicted_overshoot <= self.acceptance_criteria['max_predicted_overshoot']

        # Check 4: Simulation validation (if available)
        simulation_ok = True
        measured_overshoot = None
        if 'overshoot_measurement' in workflow_result:
            overshoot_data = workflow_result['overshoot_measurement']
            measured_overshoot = overshoot_data.get('measured_overshoot_percent', 0)
            simulation_ok = measured_overshoot <= self.acceptance_criteria['simulation_overshoot_limit']

        # Overall assessment
        all_checks_pass = lambda_bounds_ok and damping_ok and overshoot_prediction_ok and simulation_ok

        if all_checks_pass:
            result.status = 'PASSED'
            result.message = f'Issue #2 compliance verified: predicted overshoot {predicted_overshoot:.2f}%'
        else:
            result.status = 'FAILED'
            failed_checks = []
            if not lambda_bounds_ok:
                failed_checks.append(f'Lambda bounds: λ₁={lambda1:.3f}, λ₂={lambda2:.3f} > {self.acceptance_criteria["max_lambda_bounds"]}')
            if not damping_ok:
                failed_checks.append(f'Damping ratios: ζ₁={zeta1:.3f}, ζ₂={zeta2:.3f} < {self.acceptance_criteria["min_damping_ratio"]}')
            if not overshoot_prediction_ok:
                failed_checks.append(f'Predicted overshoot: {predicted_overshoot:.2f}% > {self.acceptance_criteria["max_predicted_overshoot"]}%')
            if not simulation_ok and measured_overshoot is not None:
                failed_checks.append(f'Measured overshoot: {measured_overshoot:.2f}% > {self.acceptance_criteria["simulation_overshoot_limit"]}%')
            result.message = f'Issue #2 compliance failed: {"; ".join(failed_checks)}'

        # Add detailed metrics
        result.metrics = {
            'lambda1': lambda1,
            'lambda2': lambda2,
            'damping_ratio_1': zeta1,
            'damping_ratio_2': zeta2,
            'predicted_overshoot_percent': predicted_overshoot,
            'measured_overshoot_percent': measured_overshoot,
            'lambda_bounds_compliant': lambda_bounds_ok,
            'damping_compliant': damping_ok,
            'overshoot_prediction_compliant': overshoot_prediction_ok,
            'simulation_compliant': simulation_ok
        }

        return result