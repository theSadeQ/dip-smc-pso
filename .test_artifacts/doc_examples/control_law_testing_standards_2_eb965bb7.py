# Example from: docs\control_law_testing_standards.md
# Index: 2
# Runnable: False
# Hash: eb965bb7

class SlidingSurfaceReachabilityTestSuite:
    """Test suite for sliding surface reachability verification."""

    def test_finite_time_reachability(self) -> ReachabilityTestResult:
        """Test finite-time reachability property."""

        reachability_scenarios = self._generate_reachability_scenarios()
        test_results = []

        for scenario in reachability_scenarios:
            # Compute initial sliding surface value
            s0 = self.controller.compute_sliding_surface(
                scenario.initial_state, scenario.target_state
            )

            if abs(s0) < SLIDING_SURFACE_TOLERANCE:
                continue  # Already on sliding surface

            # Simulate trajectory to sliding surface
            reaching_result = self._simulate_reaching_phase(scenario)

            # Verify reachability condition throughout trajectory
            reachability_validated = self._validate_reachability_condition(
                reaching_result.trajectory, scenario
            )

            test_results.append(ReachabilityTestCase(
                scenario=scenario,
                initial_sliding_surface=s0,
                reaching_time=reaching_result.reaching_time,
                theoretical_bound=self._calculate_theoretical_reaching_time(s0, scenario),
                reachability_condition_satisfied=reachability_validated,
                trajectory_analysis=reaching_result.trajectory_analysis
            ))

        return ReachabilityTestResult(
            test_cases=test_results,
            overall_reachability=all(tc.reachability_condition_satisfied for tc in test_results),
            finite_time_convergence=all(tc.reaching_time < float('inf') for tc in test_results),
            mathematical_property_verified=self._assess_reachability_property(test_results)
        )

    def _validate_reachability_condition(self,
                                        trajectory: List[StatePoint],
                                        scenario: ReachabilityScenario) -> bool:
        """Validate reachability condition s·ṡ ≤ -η|s| along trajectory."""

        for state_point in trajectory:
            if state_point.reached_sliding_surface:
                break  # Stop validation after reaching surface

            s = self.controller.compute_sliding_surface(
                state_point.state, scenario.target_state
            )
            s_dot = self.controller.compute_surface_derivative(
                state_point.state, scenario.target_state
            )

            # Reachability condition
            reaching_term = s * s_dot
            required_reaching_rate = -self.controller.reaching_parameter * abs(s)

            if reaching_term > required_reaching_rate + NUMERICAL_TOLERANCE:
                return False

        return True