# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 5
# Runnable: True
# Hash: 38478066

class PostOptimizationValidator:
    """
    Comprehensive validation of PSO optimization results.
    """

    def __init__(self, config: dict, controller_type: str):
        self.config = config
        self.controller_type = controller_type
        self.validation_criteria = self._load_validation_criteria()

    def validate_optimization_results(self, optimization_result: dict) -> ValidationReport:
        """
        Comprehensive validation of PSO optimization results.

        Validation Components:
        1. Mathematical consistency verification
        2. Controller-specific constraint compliance
        3. Performance benchmark comparison
        4. Issue #2 overshoot validation (STA-SMC)
        5. Safety and operational limits checking
        6. Convergence quality assessment
        """
        report = ValidationReport()

        # Extract optimization results
        best_gains = optimization_result['best_gains']
        best_cost = optimization_result['best_cost']
        cost_history = optimization_result['cost_history']

        # Validation 1: Mathematical Consistency
        math_result = self._validate_mathematical_consistency(best_gains)
        report.add_validation_result('mathematical_consistency', math_result)

        # Validation 2: Controller-Specific Constraints
        constraint_result = self._validate_controller_constraints(best_gains)
        report.add_validation_result('controller_constraints', constraint_result)

        # Validation 3: Performance Benchmarks
        performance_result = self._validate_performance_benchmarks(best_cost, cost_history)
        report.add_validation_result('performance_benchmarks', performance_result)

        # Validation 4: Issue #2 Compliance (STA-SMC specific)
        if self.controller_type == 'sta_smc':
            issue2_result = self._validate_issue2_compliance(best_gains)
            report.add_validation_result('issue2_compliance', issue2_result)

        # Validation 5: Safety and Operational Limits
        safety_result = self._validate_safety_limits(best_gains)
        report.add_validation_result('safety_limits', safety_result)

        # Validation 6: Convergence Quality
        convergence_result = self._validate_convergence_quality(cost_history)
        report.add_validation_result('convergence_quality', convergence_result)

        # Generate overall assessment
        report.generate_overall_assessment()

        return report

    def _validate_issue2_compliance(self, gains: np.ndarray) -> ValidationResult:
        """
        Validate Issue #2 overshoot compliance for STA-SMC gains.
        """
        if len(gains) < 6:
            return ValidationResult(
                is_valid=False,
                errors=['Insufficient gains for STA-SMC validation'],
                severity='CRITICAL'
            )

        K1, K2, k1, k2, lambda1, lambda2 = gains[:6]
        errors = []
        warnings = []

        # STA stability condition: K₁ > K₂
        if K1 <= K2:
            errors.append(f'STA stability violation: K₁ ({K1:.3f}) ≤ K₂ ({K2:.3f})')

        # Issue #2 damping ratio requirement: ζ ≥ 0.69
        zeta1 = lambda1 / (2 * np.sqrt(k1))
        zeta2 = lambda2 / (2 * np.sqrt(k2))

        if zeta1 < 0.69:
            errors.append(f'Issue #2 violation: ζ₁ = {zeta1:.3f} < 0.69 (may cause overshoot)')
        if zeta2 < 0.69:
            errors.append(f'Issue #2 violation: ζ₂ = {zeta2:.3f} < 0.69 (may cause overshoot)')

        # Lambda bounds check (Issue #2 prevention)
        if lambda1 > 10.0:
            warnings.append(f'Lambda1 = {lambda1:.3f} > 10.0 (Issue #2 risk)')
        if lambda2 > 10.0:
            warnings.append(f'Lambda2 = {lambda2:.3f} > 10.0 (Issue #2 risk)')

        # Predicted overshoot calculation
        avg_zeta = (zeta1 + zeta2) / 2
        if avg_zeta < 1.0:
            predicted_overshoot = 100 * np.exp(-avg_zeta * np.pi / np.sqrt(1 - avg_zeta**2))
        else:
            predicted_overshoot = 0.0

        # Issue #2 compliance check
        overshoot_compliant = predicted_overshoot < 5.0

        return ValidationResult(
            is_valid=(len(errors) == 0 and overshoot_compliant),
            errors=errors,
            warnings=warnings,
            metadata={
                'damping_ratios': [zeta1, zeta2],
                'predicted_overshoot': predicted_overshoot,
                'overshoot_compliant': overshoot_compliant,
                'issue2_status': 'compliant' if overshoot_compliant else 'violation'
            }
        )

    def _validate_performance_benchmarks(self, best_cost: float,
                                       cost_history: list) -> ValidationResult:
        """
        Validate optimization performance against established benchmarks.
        """
        benchmarks = self.validation_criteria['performance_benchmarks'][self.controller_type]
        errors = []
        warnings = []

        # Cost quality check
        expected_cost_range = benchmarks['final_cost_range']
        if not (expected_cost_range[0] <= best_cost <= expected_cost_range[1]):
            if best_cost > expected_cost_range[1]:
                errors.append(f'Poor optimization: cost {best_cost:.6f} > expected max {expected_cost_range[1]:.6f}')
            else:
                warnings.append(f'Unexpectedly good cost: {best_cost:.6f} < expected min {expected_cost_range[0]:.6f}')

        # Convergence speed check
        convergence_iterations = len(cost_history)
        expected_convergence = benchmarks['convergence_iterations']
        if convergence_iterations > expected_convergence * 1.5:
            warnings.append(f'Slow convergence: {convergence_iterations} > expected {expected_convergence}')

        # Convergence quality assessment
        if len(cost_history) >= 10:
            final_costs = cost_history[-10:]
            cost_variance = np.var(final_costs)
            if cost_variance > 1e-6:
                warnings.append(f'Unstable convergence: final cost variance {cost_variance:.2e}')

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={
                'final_cost': best_cost,
                'convergence_iterations': convergence_iterations,
                'benchmark_comparison': {
                    'cost_within_range': expected_cost_range[0] <= best_cost <= expected_cost_range[1],
                    'convergence_acceptable': convergence_iterations <= expected_convergence * 1.5
                }
            }
        )

    def simulate_and_verify_performance(self, gains: np.ndarray) -> SimulationValidationResult:
        """
        Simulate optimized controller and verify actual performance.
        """
        result = SimulationValidationResult()

        try:
            # Create controller with optimized gains
            controller = self._create_test_controller(gains)

            # Run verification simulations
            test_conditions = self.validation_criteria['test_conditions']
            for condition in test_conditions:
                sim_result = self._run_verification_simulation(controller, condition)
                result.add_simulation_result(condition['name'], sim_result)

            # Issue #2 specific overshoot measurement for STA-SMC
            if self.controller_type == 'sta_smc':
                overshoot_result = self._measure_actual_overshoot(controller)
                result.overshoot_measurement = overshoot_result

            result.overall_success = all(sim.success for sim in result.simulation_results.values())

        except Exception as e:
            result.overall_success = False
            result.error_message = str(e)

        return result

    def _measure_actual_overshoot(self, controller) -> dict:
        """
        Measure actual overshoot for Issue #2 compliance verification.
        """
        from src.simulation.core.simulation_runner import SimulationRunner

        # Standard step response test
        initial_state = np.array([0.0, 0.1, 0.0, 0.0, 0.0, 0.0])  # 0.1 rad initial angle
        target_state = np.zeros(6)

        runner = SimulationRunner(
            controller=controller,
            dynamics=self._create_test_dynamics(),
            config=self.config
        )

        # Run simulation
        sim_result = runner.run_simulation(
            initial_state=initial_state,
            duration=10.0,
            dt=0.01
        )

        # Analyze overshoot
        time_series = sim_result['time']
        angle1_series = sim_result['states'][:, 0]  # First pendulum angle

        # Find peak overshoot
        steady_state_value = angle1_series[-100:].mean()  # Last 1 second average
        peak_value = np.max(np.abs(angle1_series))
        overshoot_percent = (peak_value - abs(steady_state_value)) / 0.1 * 100  # Relative to initial 0.1 rad

        return {
            'measured_overshoot_percent': overshoot_percent,
            'peak_value': peak_value,
            'steady_state_value': steady_state_value,
            'issue2_compliant': overshoot_percent < 5.0,
            'time_series': time_series,
            'angle_series': angle1_series
        }