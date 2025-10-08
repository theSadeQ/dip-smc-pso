# Example from: docs\mathematical_validation_procedures.md
# Index: 9
# Runnable: False
# Hash: 89477ccf

def validate_timing_jitter_and_latency(control_loop: ControlLoop,
                                     jitter_requirements: JitterRequirements) -> JitterValidationResult:
    """
    Validate timing jitter and latency characteristics.

    Mathematical Foundation:
    - Jitter probability: P(jitter > J_max) ≤ ε_acceptable
    - Latency distribution analysis
    - Phase margin impact assessment
    """

    # Collect timing measurements
    timing_measurements = []

    for _ in range(NUM_JITTER_MEASUREMENTS):
        measurement = control_loop.run_single_iteration_with_timing()
        timing_measurements.append(measurement)

    # Extract timing components
    sensor_latencies = [m.sensor_latency for m in timing_measurements]
    computation_times = [m.computation_time for m in timing_measurements]
    actuator_latencies = [m.actuator_latency for m in timing_measurements]
    total_latencies = [m.total_latency for m in timing_measurements]

    # Jitter analysis (timing variability)
    def analyze_jitter(times: List[float], component_name: str) -> JitterAnalysis:
        times_array = np.array(times)

        # Calculate jitter metrics
        mean_time = np.mean(times_array)
        jitter_std = np.std(times_array)
        max_jitter = np.max(times_array) - np.min(times_array)

        # Jitter probability analysis
        jitter_threshold = jitter_requirements.max_acceptable_jitter[component_name]
        jitter_violations = times_array[times_array > mean_time + jitter_threshold]
        jitter_violation_probability = len(jitter_violations) / len(times_array)

        return JitterAnalysis(
            component=component_name,
            mean_time=mean_time,
            jitter_std=jitter_std,
            max_jitter=max_jitter,
            jitter_violation_probability=jitter_violation_probability,
            acceptable_jitter=jitter_violation_probability <= jitter_requirements.acceptable_violation_probability
        )

    # Analyze jitter for each component
    jitter_analyses = {
        'sensor': analyze_jitter(sensor_latencies, 'sensor'),
        'computation': analyze_jitter(computation_times, 'computation'),
        'actuator': analyze_jitter(actuator_latencies, 'actuator'),
        'total': analyze_jitter(total_latencies, 'total')
    }

    # Control system impact analysis
    control_impact = _analyze_jitter_control_impact(
        jitter_analyses, control_loop.controller_parameters
    )

    return JitterValidationResult(
        jitter_analyses=jitter_analyses,
        control_impact=control_impact,
        overall_timing_acceptable=all(j.acceptable_jitter for j in jitter_analyses.values()),
        mathematical_interpretation=_interpret_jitter_results(jitter_analyses, control_impact)
    )

def _analyze_jitter_control_impact(jitter_analyses: Dict[str, JitterAnalysis],
                                 controller_params: ControllerParameters) -> ControlImpactAnalysis:
    """Analyze impact of timing jitter on control performance."""

    # Phase margin impact estimation
    total_jitter_std = jitter_analyses['total'].jitter_std
    control_frequency = controller_params.control_frequency

    # Phase delay due to jitter (in radians)
    phase_delay_std = 2 * np.pi * control_frequency * total_jitter_std

    # Estimate phase margin degradation
    nominal_phase_margin = controller_params.nominal_phase_margin
    phase_margin_degradation = phase_delay_std
    remaining_phase_margin = nominal_phase_margin - phase_margin_degradation

    # Stability impact assessment
    if remaining_phase_margin > np.pi/6:  # 30 degrees
        stability_impact = "minimal"
    elif remaining_phase_margin > np.pi/12:  # 15 degrees
        stability_impact = "moderate"
    else:
        stability_impact = "significant"

    return ControlImpactAnalysis(
        phase_delay_std=phase_delay_std,
        phase_margin_degradation=phase_margin_degradation,
        remaining_phase_margin=remaining_phase_margin,
        stability_impact=stability_impact,
        performance_degradation_estimate=_estimate_performance_degradation(phase_margin_degradation)
    )