# Citation Request: Fault Detection Hysteresis Theorem

I need academic citations for the following theorem in fault detection and diagnosis systems.

## THEOREM STATEMENT

"Hysteresis with deadband δ prevents oscillation for residuals with bounded derivative."

## TECHNICAL CONTEXT

**Domain:** Fault Detection and Isolation (FDI) systems in control engineering

**Mathematical Background:**
- Residual signals in FDI systems are used to detect faults by monitoring system behavior
- When residuals hover near threshold boundaries, noise can cause rapid oscillations between fault/no-fault states
- Hysteresis implements two thresholds (upper and lower) with deadband δ between them
- The bounded derivative assumption means the rate of change of residual signal is limited: |dr/dt| ≤ M for some constant M

**Application:**
This theorem establishes that hysteresis thresholding with properly chosen deadband prevents chattering (rapid switching) in fault detection decisions when residual signals have bounded rates of change. This is critical for reliable fault diagnosis in real-time control systems.

## REQUIRED CITATIONS

Find 2-3 academic papers/books that:

1. **Establish mathematical foundations** for hysteresis in threshold logic or fault detection
2. **Prove or analyze** oscillation prevention properties of hysteresis switching
3. **Apply hysteresis** to residual evaluation in FDI systems for dynamic systems

**Priority topics:**
- Hysteresis switching in control systems
- Chattering prevention in threshold-based decisions
- Fault detection and isolation methodology
- Residual generation and evaluation techniques

## OUTPUT FORMAT

For each citation provide:

1. **Full Citation:** Authors, "Title," Venue, Year, Pages (if applicable)
2. **DOI or URL:** Direct link to paper
3. **Relevance:** 2-3 sentences explaining why this citation supports the theorem
4. **Key Result:** Specific theorem/equation/section number that relates to hysteresis oscillation prevention

## FOCUS AREAS

Seminal works in:
- FDI systems (Gertler, Chen, Patton, Blanke)
- Robust fault detection
- Threshold logic and hysteresis switching
- Observer-based fault detection with bounded disturbances

Provide citations that would support this theorem in an academic control systems paper.
