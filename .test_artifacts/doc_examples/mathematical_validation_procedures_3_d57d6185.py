# Example from: docs\mathematical_validation_procedures.md
# Index: 3
# Runnable: False
# Hash: d57d6185

# example-metadata:
# runnable: false

def validate_chattering_characteristics(controller: SMCController,
                                      test_scenarios: List[TestScenario]) -> ChatteringValidationResult:
    """
    Analyze and validate chattering characteristics.

    Mathematical Metrics:
    - Chattering Index: CI = (1/T)∫|u(t) - u_avg(t)|dt
    - Frequency Content: Dominant frequencies in control signal
    - Amplitude Analysis: Peak-to-peak chattering amplitude
    """

    chattering_results = []

    for scenario in test_scenarios:
        t, states, controls = simulate_with_control_history(controller, scenario)

        # Calculate chattering index
        control_signal = np.array(controls)

        # Moving average filter for averaged control
        window_size = int(0.1 / scenario.dt)  # 100ms window
        u_avg = np.convolve(control_signal, np.ones(window_size)/window_size, mode='same')

        # Chattering index calculation
        chattering_deviation = np.abs(control_signal - u_avg)
        chattering_index = np.mean(chattering_deviation)

        # Frequency analysis
        frequencies, power_spectrum = signal.welch(control_signal, fs=1/scenario.dt)
        dominant_frequency = frequencies[np.argmax(power_spectrum)]

        # Amplitude analysis
        control_range = np.max(control_signal) - np.min(control_signal)

        # Assess chattering severity
        chattering_severity = _assess_chattering_severity(
            chattering_index, dominant_frequency, control_range
        )

        chattering_results.append(ChatteringTestResult(
            scenario=scenario.name,
            chattering_index=chattering_index,
            dominant_frequency=dominant_frequency,
            control_range=control_range,
            chattering_severity=chattering_severity,
            acceptable_chattering=chattering_index < ACCEPTABLE_CHATTERING_THRESHOLD
        ))

    return ChatteringValidationResult(
        test_results=chattering_results,
        overall_chattering_acceptable=all(r.acceptable_chattering for r in chattering_results),
        average_chattering_index=np.mean([r.chattering_index for r in chattering_results]),
        mathematical_interpretation=_interpret_chattering_results(chattering_results)
    )

def _assess_chattering_severity(chattering_index: float,
                               dominant_frequency: float,
                               control_range: float) -> str:
    """Assess chattering severity based on multiple metrics."""

    # Chattering severity classification
    if chattering_index < 0.1:
        severity = "minimal"
    elif chattering_index < 0.5:
        severity = "low"
    elif chattering_index < 1.0:
        severity = "moderate"
    else:
        severity = "high"

    # Frequency considerations
    if dominant_frequency > 100:  # Hz
        severity += "_high_frequency"

    # Control range considerations
    if control_range > 0.8 * MAX_CONTROL_INPUT:
        severity += "_large_amplitude"

    return severity