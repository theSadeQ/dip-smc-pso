# Example from: docs\control_law_testing_standards.md
# Index: 4
# Runnable: False
# Hash: bfabcbb5

# example-metadata:
# runnable: false

class ControlSaturationTestSuite:
    """Safety-critical testing for control input saturation."""

    def test_control_saturation_safety(self) -> ControlSaturationTestResult:
        """Test control saturation under extreme conditions."""

        # Generate extreme test scenarios
        extreme_scenarios = self._generate_extreme_test_scenarios()
        saturation_violations = []
        saturation_test_results = []

        for scenario in extreme_scenarios:
            # Simulate under extreme conditions
            t, states, controls = self._simulate_with_control_history(scenario)

            # Check for saturation violations
            for i, control in enumerate(controls):
                if abs(control) > self.max_control_force:
                    saturation_violations.append(ControlSaturationViolation(
                        scenario=scenario.name,
                        time=t[i],
                        state=states[i],
                        control_value=control,
                        max_allowed=self.max_control_force,
                        violation_magnitude=abs(control) - self.max_control_force
                    ))

            # Analyze saturation behavior
            saturation_analysis = self._analyze_saturation_behavior(controls, scenario)

            saturation_test_results.append(ControlSaturationTestCase(
                scenario=scenario,
                max_control_used=np.max(np.abs(controls)),
                control_margin=self.max_control_force - np.max(np.abs(controls)),
                saturation_violations=len([v for v in saturation_violations if v.scenario == scenario.name]),
                saturation_analysis=saturation_analysis,
                safety_requirements_met=np.max(np.abs(controls)) <= self.max_control_force
            ))

        return ControlSaturationTestResult(
            test_cases=saturation_test_results,
            total_violations=len(saturation_violations),
            safety_critical_requirements_met=len(saturation_violations) == 0,
            control_safety_verified=all(tc.safety_requirements_met for tc in saturation_test_results)
        )

    def _generate_extreme_test_scenarios(self) -> List[ExtremeTestScenario]:
        """Generate extreme scenarios for safety testing."""

        scenarios = []

        # Scenario 1: Maximum initial angle displacement
        scenarios.append(ExtremeTestScenario(
            name="maximum_angle_displacement",
            initial_state=np.array([np.pi/2, np.pi/3, 0.0, 0.0, 0.0, 0.0]),
            disturbances=None,
            test_duration=15.0,
            safety_criticality="high"
        ))

        # Scenario 2: High velocity initial conditions
        scenarios.append(ExtremeTestScenario(
            name="high_velocity_initial",
            initial_state=np.array([0.1, 0.1, 0.0, 5.0, 4.0, 2.0]),
            disturbances=None,
            test_duration=10.0,
            safety_criticality="high"
        ))

        # Scenario 3: Large cart displacement with angles
        scenarios.append(ExtremeTestScenario(
            name="large_cart_displacement",
            initial_state=np.array([0.2, 0.15, 2.0, 0.0, 0.0, 0.0]),
            disturbances=None,
            test_duration=12.0,
            safety_criticality="medium"
        ))

        # Scenario 4: External disturbances during control
        scenarios.append(ExtremeTestScenario(
            name="external_disturbances",
            initial_state=np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0]),
            disturbances=self._create_disturbance_profile(),
            test_duration=20.0,
            safety_criticality="high"
        ))

        return scenarios