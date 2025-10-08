# Example from: docs\reports\pso_code_quality_optimization_report.md
# Index: 10
# Runnable: True
# Hash: 58b6b9e9

def validate_pso_parameters(particles: np.ndarray, bounds: np.ndarray) -> bool:
    """Comprehensive PSO parameter validation with security checks."""
    if not isinstance(particles, np.ndarray):
        raise TypeError("Particles must be numpy array")

    if particles.ndim != 2:
        raise ValueError("Particles must be 2D array")

    if not np.all(np.isfinite(particles)):
        raise ValueError("Particles contain invalid values")