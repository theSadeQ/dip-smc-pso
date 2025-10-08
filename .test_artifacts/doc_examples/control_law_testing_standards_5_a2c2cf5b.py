# Example from: docs\control_law_testing_standards.md
# Index: 5
# Runnable: False
# Hash: a2c2cf5b

class StateConstraintTestSuite:
    """Test suite for state constraint verification."""

    def test_state_constraint_satisfaction(self) -> StateConstraintTestResult:
        """Test state constraint satisfaction under various conditions."""

        # Define state constraints
        state_constraints = StateConstraints(
            angle_limits=(-np.pi, np.pi),           # ±180 degrees
            velocity_limits=(-10.0, 10.0),         # ±10 rad/s
            cart_position_limits=(-3.0, 3.0),      # ±3 meters
            cart_velocity_limits=(-5.0, 5.0)       # ±5 m/s
        )

        constraint_test_scenarios = self._generate_constraint_test_scenarios()
        constraint_violations = []
        test_results = []

        for scenario in constraint_test_scenarios:
            # Simulate system response
            t, states = self._simulate_control_response(scenario)

            # Check constraints at each time step
            scenario_violations = []
            for i, state in enumerate(states):
                violations = self._check_state_constraints(state, state_constraints)
                if violations:
                    for violation in violations:
                        violation.time = t[i]
                        violation.scenario = scenario.name
                        scenario_violations.append(violation)
                        constraint_violations.append(violation)

            # Analyze constraint behavior
            constraint_analysis = self._analyze_constraint_behavior(states, state_constraints)

            test_results.append(StateConstraintTestCase(
                scenario=scenario,
                constraint_violations=scenario_violations,
                constraint_margins=constraint_analysis.constraint_margins,
                worst_case_states=constraint_analysis.worst_case_states,
                constraints_satisfied=len(scenario_violations) == 0
            ))

        return StateConstraintTestResult(
            test_cases=test_results,
            total_constraint_violations=len(constraint_violations),
            constraint_types_violated=self._categorize_violations(constraint_violations),
            safety_constraints_satisfied=len(constraint_violations) == 0
        )

    def _check_state_constraints(self,
                                state: np.ndarray,
                                constraints: StateConstraints) -> List[StateConstraintViolation]:
        """Check if state violates any constraints."""

        violations = []
        θ1, θ2, x, θ1_dot, θ2_dot, x_dot = state

        # Angle constraints
        if not (constraints.angle_limits[0] <= θ1 <= constraints.angle_limits[1]):
            violations.append(StateConstraintViolation(
                constraint_type="angle_limit",
                variable="theta1",
                value=θ1,
                limit=constraints.angle_limits,
                violation_magnitude=max(θ1 - constraints.angle_limits[1],
                                      constraints.angle_limits[0] - θ1)
            ))

        if not (constraints.angle_limits[0] <= θ2 <= constraints.angle_limits[1]):
            violations.append(StateConstraintViolation(
                constraint_type="angle_limit",
                variable="theta2",
                value=θ2,
                limit=constraints.angle_limits,
                violation_magnitude=max(θ2 - constraints.angle_limits[1],
                                      constraints.angle_limits[0] - θ2)
            ))

        # Velocity constraints
        if not (constraints.velocity_limits[0] <= θ1_dot <= constraints.velocity_limits[1]):
            violations.append(StateConstraintViolation(
                constraint_type="velocity_limit",
                variable="theta1_dot",
                value=θ1_dot,
                limit=constraints.velocity_limits,
                violation_magnitude=max(θ1_dot - constraints.velocity_limits[1],
                                      constraints.velocity_limits[0] - θ1_dot)
            ))

        # Cart position constraints
        if not (constraints.cart_position_limits[0] <= x <= constraints.cart_position_limits[1]):
            violations.append(StateConstraintViolation(
                constraint_type="position_limit",
                variable="cart_position",
                value=x,
                limit=constraints.cart_position_limits,
                violation_magnitude=max(x - constraints.cart_position_limits[1],
                                      constraints.cart_position_limits[0] - x)
            ))

        return violations