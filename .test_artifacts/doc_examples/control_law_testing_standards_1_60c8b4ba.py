# Example from: docs\control_law_testing_standards.md
# Index: 1
# Runnable: False
# Hash: 60c8b4ba

# example-metadata:
# runnable: false

class LyapunovStabilityTestSuite:
    """Comprehensive Lyapunov stability test suite for SMC controllers."""

    def __init__(self, controller: SMCController):
        self.controller = controller
        self.test_scenarios = self._generate_stability_test_scenarios()
        self.tolerance = 1e-8

    def _generate_stability_test_scenarios(self) -> List[StabilityTestScenario]:
        """Generate comprehensive test scenarios for stability verification."""

        scenarios = []

        # Scenario 1: Small angle perturbations
        scenarios.append(StabilityTestScenario(
            name="small_angle_perturbations",
            initial_states=self._generate_small_angle_states(),
            target_state=np.zeros(6),
            test_duration=5.0,
            mathematical_property="small_angle_stability"
        ))

        # Scenario 2: Large angle perturbations
        scenarios.append(StabilityTestScenario(
            name="large_angle_perturbations",
            initial_states=self._generate_large_angle_states(),
            target_state=np.zeros(6),
            test_duration=10.0,
            mathematical_property="large_angle_stability"
        ))

        # Scenario 3: High velocity initial conditions
        scenarios.append(StabilityTestScenario(
            name="high_velocity_conditions",
            initial_states=self._generate_high_velocity_states(),
            target_state=np.zeros(6),
            test_duration=8.0,
            mathematical_property="high_energy_stability"
        ))

        # Scenario 4: Cart position perturbations
        scenarios.append(StabilityTestScenario(
            name="cart_position_perturbations",
            initial_states=self._generate_cart_position_states(),
            target_state=np.zeros(6),
            test_duration=6.0,
            mathematical_property="cart_stabilization"
        ))

        return scenarios

    def test_lyapunov_stability_comprehensive(self) -> LyapunovTestResult:
        """Execute comprehensive Lyapunov stability testing."""

        all_test_results = []
        stability_violations = []

        for scenario in self.test_scenarios:
            scenario_results = []

            for initial_state in scenario.initial_states:
                # Simulate system response
                t, states = self._simulate_control_response(
                    initial_state, scenario.target_state, scenario.test_duration
                )

                # Verify Lyapunov condition at each time step
                for i, state in enumerate(states):
                    lyapunov_result = self._verify_lyapunov_condition(
                        state, scenario.target_state, t[i]
                    )

                    scenario_results.append(lyapunov_result)

                    if not lyapunov_result.stability_satisfied:
                        stability_violations.append(StabilityViolation(
                            scenario=scenario.name,
                            time=t[i],
                            state=state,
                            sliding_surface=lyapunov_result.sliding_surface,
                            lyapunov_derivative=lyapunov_result.lyapunov_derivative,
                            violation_magnitude=lyapunov_result.lyapunov_derivative
                        ))

            all_test_results.extend(scenario_results)

        # Calculate stability metrics
        total_test_points = len(all_test_results)
        stable_points = len([r for r in all_test_results if r.stability_satisfied])
        stability_percentage = (stable_points / total_test_points) * 100

        return LyapunovTestResult(
            total_test_points=total_test_points,
            stable_points=stable_points,
            stability_percentage=stability_percentage,
            stability_violations=stability_violations,
            mathematical_property_verified=stability_percentage >= 99.9,
            test_coverage_complete=True,
            mathematical_interpretation=self._interpret_stability_results(
                stability_percentage, stability_violations
            )
        )

    def _verify_lyapunov_condition(self,
                                  state: np.ndarray,
                                  target: np.ndarray,
                                  time: float) -> LyapunovTestPoint:
        """Verify Lyapunov stability condition at a single point."""

        # Compute sliding surface value
        sliding_surface = self.controller.compute_sliding_surface(state, target)

        # Skip verification if on sliding surface (within tolerance)
        if abs(sliding_surface) < self.tolerance:
            return LyapunovTestPoint(
                time=time,
                state=state,
                sliding_surface=sliding_surface,
                lyapunov_derivative=0.0,
                stability_satisfied=True,
                on_sliding_surface=True
            )

        # Compute sliding surface time derivative
        surface_derivative = self.controller.compute_surface_derivative(state, target)

        # Lyapunov stability condition: V̇ = s·ṡ < 0
        lyapunov_derivative = sliding_surface * surface_derivative
        stability_satisfied = lyapunov_derivative < -self.tolerance

        return LyapunovTestPoint(
            time=time,
            state=state,
            sliding_surface=sliding_surface,
            surface_derivative=surface_derivative,
            lyapunov_derivative=lyapunov_derivative,
            stability_satisfied=stability_satisfied,
            on_sliding_surface=False
        )