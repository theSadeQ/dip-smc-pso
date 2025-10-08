# Example from: docs\control_law_testing_standards.md
# Index: 7
# Runnable: False
# Hash: cb495b75

# example-metadata:
# runnable: false

class RobustnessTestSuite:
    """Test suite for control robustness verification."""

    def test_parameter_uncertainty_robustness(self) -> RobustnessTestResult:
        """Test robustness to parameter uncertainties."""

        # Define parameter uncertainty ranges
        parameter_uncertainties = ParameterUncertainties(
            mass_uncertainty=0.2,      # ±20%
            length_uncertainty=0.1,    # ±10%
            friction_uncertainty=0.5,  # ±50%
            inertia_uncertainty=0.15   # ±15%
        )

        robustness_scenarios = self._generate_robustness_scenarios(parameter_uncertainties)
        robustness_results = []

        for scenario in robustness_scenarios:
            # Test with perturbed parameters
            perturbed_results = []

            for parameter_set in scenario.parameter_variations:
                # Create system with perturbed parameters
                perturbed_system = self._create_perturbed_system(parameter_set)

                # Test control performance
                performance = self._test_control_performance(
                    perturbed_system, scenario.test_conditions
                )

                perturbed_results.append(RobustnessTestCase(
                    parameter_variation=parameter_set,
                    performance_degradation=self._calculate_performance_degradation(
                        performance, scenario.nominal_performance
                    ),
                    stability_maintained=performance.stable,
                    robustness_margin=self._calculate_robustness_margin(performance)
                ))

            # Analyze robustness characteristics
            robustness_analysis = self._analyze_robustness_characteristics(perturbed_results)

            robustness_results.append(RobustnessScenarioResult(
                scenario=scenario,
                test_cases=perturbed_results,
                robustness_analysis=robustness_analysis,
                robust_performance_maintained=robustness_analysis.robust_performance
            ))

        return RobustnessTestResult(
            scenario_results=robustness_results,
            overall_robustness=all(sr.robust_performance_maintained for sr in robustness_results),
            robustness_summary=self._summarize_robustness(robustness_results)
        )

    def test_disturbance_rejection(self) -> DisturbanceRejectionTestResult:
        """Test disturbance rejection capabilities."""

        disturbance_scenarios = self._generate_disturbance_scenarios()
        rejection_results = []

        for scenario in disturbance_scenarios:
            # Simulate with disturbances
            t, states, disturbances = self._simulate_with_disturbances(scenario)

            # Analyze disturbance rejection
            rejection_analysis = self._analyze_disturbance_rejection(
                t, states, disturbances, scenario
            )

            rejection_results.append(DisturbanceRejectionTestCase(
                scenario=scenario,
                rejection_analysis=rejection_analysis,
                disturbance_attenuation=rejection_analysis.attenuation_factor,
                recovery_time=rejection_analysis.recovery_time,
                disturbance_rejection_adequate=rejection_analysis.adequate_rejection
            ))

        return DisturbanceRejectionTestResult(
            test_cases=rejection_results,
            overall_disturbance_rejection=all(tc.disturbance_rejection_adequate for tc in rejection_results),
            rejection_summary=self._summarize_disturbance_rejection(rejection_results)
        )