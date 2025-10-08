# Example from: docs\control_law_testing_standards.md
# Index: 6
# Runnable: False
# Hash: 93e34d20

# example-metadata:
# runnable: false

class ControlObjectiveTestSuite:
    """Test suite for control objective verification."""

    def test_control_objectives_achievement(self) -> ControlObjectiveTestResult:
        """Test achievement of control objectives."""

        # Define control objectives
        control_objectives = ControlObjectives(
            settling_time_requirement=5.0,          # seconds
            overshoot_requirement=0.1,             # 10%
            steady_state_error_requirement=0.01,   # 1% of reference
            rise_time_requirement=2.0              # seconds
        )

        objective_test_scenarios = self._generate_objective_test_scenarios()
        test_results = []

        for scenario in objective_test_scenarios:
            # Simulate step response
            t, states = self._simulate_step_response(scenario)

            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(
                t, states, scenario.reference_trajectory, control_objectives
            )

            # Verify objectives
            objectives_met = self._verify_control_objectives(
                performance_metrics, control_objectives
            )

            test_results.append(ControlObjectiveTestCase(
                scenario=scenario,
                performance_metrics=performance_metrics,
                objectives_met=objectives_met,
                control_quality_score=self._calculate_control_quality_score(performance_metrics)
            ))

        return ControlObjectiveTestResult(
            test_cases=test_results,
            overall_objectives_met=all(tc.objectives_met.all_objectives_satisfied for tc in test_results),
            performance_summary=self._summarize_performance(test_results)
        )

    def _calculate_performance_metrics(self,
                                     time: np.ndarray,
                                     states: np.ndarray,
                                     reference: np.ndarray,
                                     objectives: ControlObjectives) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics."""

        # Extract angle trajectories (primary control variables)
        θ1_trajectory = states[:, 0]
        θ2_trajectory = states[:, 1]

        # Calculate settling time
        settling_time = self._calculate_settling_time(
            time, θ1_trajectory, objectives.steady_state_error_requirement
        )

        # Calculate overshoot
        overshoot = self._calculate_overshoot(θ1_trajectory)

        # Calculate rise time
        rise_time = self._calculate_rise_time(time, θ1_trajectory)

        # Calculate steady-state error
        steady_state_error = self._calculate_steady_state_error(
            θ1_trajectory, reference[0]
        )

        # Calculate ISE (Integral of Squared Error)
        ise = self._calculate_ise(time, states, reference)

        # Calculate ITAE (Integral of Time-weighted Absolute Error)
        itae = self._calculate_itae(time, states, reference)

        return PerformanceMetrics(
            settling_time=settling_time,
            overshoot=overshoot,
            rise_time=rise_time,
            steady_state_error=steady_state_error,
            ise=ise,
            itae=itae,
            control_energy=self._calculate_control_energy(time, states)
        )

    def _verify_control_objectives(self,
                                  metrics: PerformanceMetrics,
                                  objectives: ControlObjectives) -> ObjectiveVerificationResult:
        """Verify control objectives are met."""

        settling_time_met = metrics.settling_time <= objectives.settling_time_requirement
        overshoot_met = metrics.overshoot <= objectives.overshoot_requirement
        steady_state_error_met = metrics.steady_state_error <= objectives.steady_state_error_requirement
        rise_time_met = metrics.rise_time <= objectives.rise_time_requirement

        return ObjectiveVerificationResult(
            settling_time_met=settling_time_met,
            overshoot_met=overshoot_met,
            steady_state_error_met=steady_state_error_met,
            rise_time_met=rise_time_met,
            all_objectives_satisfied=all([
                settling_time_met, overshoot_met, steady_state_error_met, rise_time_met
            ]),
            objective_margins=self._calculate_objective_margins(metrics, objectives)
        )