# Example from: docs\fault_detection_system_documentation.md
# Index: 21
# Runnable: False
# Hash: c59d0b02

# example-metadata:
# runnable: false

def diagnose_false_alarms(fdi_system):
    """Diagnostic procedure for false alarm investigation."""

    # Check threshold appropriateness
    residual_stats = np.array(fdi_system.residuals[-100:])  # Recent residuals
    mean_residual = np.mean(residual_stats)
    std_residual = np.std(residual_stats)

    recommended_threshold = mean_residual + 3 * std_residual

    print(f"Current threshold: {fdi_system.residual_threshold}")
    print(f"Recommended threshold: {recommended_threshold:.4f}")
    print(f"Residual statistics: μ={mean_residual:.4f}, σ={std_residual:.4f}")

    # Check noise characterization
    if std_residual > 0.1 * mean_residual:
        print("WARNING: High residual noise detected")
        print("RECOMMENDATION: Enable adaptive thresholding")

    # Check persistence counter
    violation_rate = sum(r > fdi_system.residual_threshold for r in residual_stats) / len(residual_stats)
    if violation_rate > 0.1:  # > 10% violation rate
        print(f"High violation rate: {violation_rate:.2%}")
        print("RECOMMENDATION: Increase persistence counter or threshold")