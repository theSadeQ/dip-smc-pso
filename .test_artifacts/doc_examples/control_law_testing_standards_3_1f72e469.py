# Example from: docs\control_law_testing_standards.md
# Index: 3
# Runnable: False
# Hash: 1f72e469

class ConvergenceRateTestSuite:
    """Test suite for convergence rate verification."""

    def test_exponential_convergence_rate(self) -> ConvergenceRateTestResult:
        """Test exponential convergence rate properties."""

        convergence_scenarios = self._generate_convergence_scenarios()
        rate_test_results = []

        for scenario in convergence_scenarios:
            # Simulate closed-loop response
            t, states = self._simulate_convergence_response(scenario)

            # Extract convergence metric (error norm)
            error_trajectory = [
                np.linalg.norm(state - scenario.target_state)
                for state in states
            ]

            # Fit exponential decay model: ||e(t)|| = ||e₀|| * exp(-λt)
            convergence_analysis = self._analyze_exponential_convergence(
                t, error_trajectory
            )

            # Verify convergence rate meets specifications
            rate_specification_met = self._verify_convergence_rate_specification(
                convergence_analysis, scenario.required_convergence_rate
            )

            rate_test_results.append(ConvergenceRateTestCase(
                scenario=scenario,
                measured_convergence_rate=convergence_analysis.convergence_rate,
                required_convergence_rate=scenario.required_convergence_rate,
                rate_specification_met=rate_specification_met,
                convergence_analysis=convergence_analysis,
                mathematical_model_fit=convergence_analysis.model_fit_quality
            ))

        return ConvergenceRateTestResult(
            test_cases=rate_test_results,
            overall_convergence_rate_verified=all(tc.rate_specification_met for tc in rate_test_results),
            mathematical_property_verified=self._assess_convergence_property(rate_test_results)
        )

    def _analyze_exponential_convergence(self,
                                        time: np.ndarray,
                                        error_trajectory: List[float]) -> ConvergenceAnalysis:
        """Analyze exponential convergence characteristics."""

        error_array = np.array(error_trajectory)

        # Remove zero or very small errors to avoid log issues
        valid_indices = error_array > CONVERGENCE_TOLERANCE
        valid_times = time[valid_indices]
        valid_errors = error_array[valid_indices]

        if len(valid_errors) < 10:
            return ConvergenceAnalysis(
                convergence_rate=0.0,
                model_fit_quality=0.0,
                exponential_fit_valid=False
            )

        # Fit exponential model: log(e(t)) = log(e₀) - λt
        log_errors = np.log(valid_errors)
        coefficients = np.polyfit(valid_times, log_errors, 1)
        convergence_rate = -coefficients[0]  # λ = -slope

        # Assess model fit quality
        predicted_log_errors = np.polyval(coefficients, valid_times)
        r_squared = self._calculate_r_squared(log_errors, predicted_log_errors)

        return ConvergenceAnalysis(
            convergence_rate=convergence_rate,
            initial_error=valid_errors[0],
            final_error=valid_errors[-1],
            model_fit_quality=r_squared,
            exponential_fit_valid=r_squared > 0.95,
            time_to_convergence=self._estimate_convergence_time(
                valid_errors[0], convergence_rate
            )
        )