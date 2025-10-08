# Example from: docs\fault_detection_system_documentation.md
# Index: 23
# Runnable: False
# Hash: c0030fd8

def optimize_fdi_performance(fdi_system):
    """Performance optimization recommendations."""

    # Check window size
    if fdi_system.window_size > 100:
        print("RECOMMENDATION: Reduce window_size for faster adaptation")

    # Check history growth
    if len(fdi_system.times) > 100000:
        print("WARNING: Large history detected")
        print("RECOMMENDATION: Implement history truncation")

        # Example truncation
        keep_recent = 10000
        fdi_system.times = fdi_system.times[-keep_recent:]
        fdi_system.residuals = fdi_system.residuals[-keep_recent:]

    # Check state dimension
    if len(fdi_system.residual_states) > 10:
        print("RECOMMENDATION: Reduce number of monitored states")