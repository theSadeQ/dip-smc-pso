# Example from: docs\mathematical_validation_procedures.md
# Index: 6
# Runnable: False
# Hash: 5efdc280

# example-metadata:
# runnable: false

def validate_numerical_integration_stability(integrators: List[NumericalIntegrator],
                                           test_scenarios: List[IntegrationTestScenario]) -> NumericalStabilityResult:
    """
    Validate numerical integration stability and accuracy.

    Mathematical Foundation:
    - Energy conservation verification
    - Truncation error analysis
    - Stability region analysis
    """

    stability_results = {}

    for integrator in integrators:
        integrator_results = []

        for scenario in test_scenarios:
            # Run integration
            t, states = integrator.integrate(
                initial_state=scenario.initial_state,
                dynamics=scenario.dynamics,
                time_span=scenario.time_span,
                dt=scenario.dt
            )

            # Energy conservation analysis (for Hamiltonian systems)
            if scenario.is_conservative:
                energy_conservation = _validate_energy_conservation(
                    states, scenario.physics_params
                )
            else:
                energy_conservation = None

            # Truncation error estimation
            truncation_error = _estimate_truncation_error(
                integrator, scenario, reference_solution=scenario.reference_solution
            )

            # Stability analysis
            stability_analysis = _analyze_numerical_stability(
                states, scenario.dt, integrator.stability_region
            )

            integrator_results.append(IntegrationTestResult(
                scenario=scenario.name,
                energy_conservation=energy_conservation,
                truncation_error=truncation_error,
                stability_analysis=stability_analysis,
                numerical_accuracy=_calculate_numerical_accuracy(states, scenario.reference_solution)
            ))

        stability_results[integrator.name] = integrator_results

    return NumericalStabilityResult(
        integrator_results=stability_results,
        overall_stability=_assess_overall_numerical_stability(stability_results),
        mathematical_interpretation=_interpret_numerical_stability(stability_results)
    )

def _validate_energy_conservation(states: np.ndarray,
                                physics_params: PhysicsParameters) -> EnergyConservationResult:
    """Validate energy conservation for Hamiltonian systems."""

    energies = []

    for state in states:
        # Calculate kinetic energy
        q = state[:3]  # [θ₁, θ₂, x]
        q_dot = state[3:]  # [θ̇₁, θ̇₂, ẋ]

        # Mass matrix for double inverted pendulum
        M = calculate_mass_matrix(q, physics_params)
        kinetic_energy = 0.5 * q_dot.T @ M @ q_dot

        # Potential energy
        potential_energy = calculate_potential_energy(q, physics_params)

        # Total energy
        total_energy = kinetic_energy + potential_energy
        energies.append(total_energy)

    energies = np.array(energies)
    initial_energy = energies[0]

    # Energy drift analysis
    energy_drift = energies - initial_energy
    max_absolute_drift = np.max(np.abs(energy_drift))
    max_relative_drift = max_absolute_drift / abs(initial_energy) if initial_energy != 0 else max_absolute_drift

    # Energy conservation quality
    if max_relative_drift < 1e-6:
        conservation_quality = "excellent"
    elif max_relative_drift < 1e-4:
        conservation_quality = "good"
    elif max_relative_drift < 1e-2:
        conservation_quality = "acceptable"
    else:
        conservation_quality = "poor"

    return EnergyConservationResult(
        initial_energy=initial_energy,
        final_energy=energies[-1],
        max_absolute_drift=max_absolute_drift,
        max_relative_drift=max_relative_drift,
        conservation_quality=conservation_quality,
        energy_conserved=max_relative_drift < ENERGY_CONSERVATION_TOLERANCE
    )