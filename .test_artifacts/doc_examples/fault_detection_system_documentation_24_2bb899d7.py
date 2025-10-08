# Example from: docs\fault_detection_system_documentation.md
# Index: 24
# Runnable: False
# Hash: 2bb899d7

# example-metadata:
# runnable: false

def characterize_system_baseline(simulation_data):
    """Establish baseline noise characteristics."""
    residuals = []

    # Run fault-free simulation
    for measurement in simulation_data['normal_operation']:
        residual = compute_residual(measurement)
        residuals.append(residual)

    baseline_stats = {
        'mean': np.mean(residuals),
        'std': np.std(residuals),
        'p95': np.percentile(residuals, 95),
        'p99': np.percentile(residuals, 99)
    }

    return baseline_stats